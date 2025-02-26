import os
import hashlib
import re
from PyQt5.QtCore import QThread, pyqtSignal
import madmom
import warnings
import numpy as np

class ChordRecognitionThread(QThread):
    result = pyqtSignal(list)
    
    # Lista para mantener un seguimiento de los archivos de caché creados durante esta sesión
    session_cache_files = []
    
    def __init__(self, audio_path, clear_cache=False):
        super().__init__()
        self.audio_path = audio_path
        self.clear_cache = clear_cache
        self.tonality_map = {}  # Para guardar frecuencias de notas y detectar tonalidad
        
    @staticmethod
    def clear_chord_cache(all_files=False):
        """
        Limpia los archivos de caché de acordes
        
        Args:
            all_files (bool): Si es True, elimina todos los archivos de caché.
                             Si es False, solo elimina los creados en esta sesión.
        """
        cache_dir = "cache/chord/"
        if not os.path.exists(cache_dir):
            print("No existe directorio de caché para limpiar")
            return
            
        if all_files:
            # Eliminar todos los archivos de caché
            for filename in os.listdir(cache_dir):
                file_path = os.path.join(cache_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error al eliminar {file_path}: {e}")
            print("Todo el caché de acordes limpiado con éxito")
        else:
            # Eliminar solo los archivos de caché creados en esta sesión
            for file_path in ChordRecognitionThread.session_cache_files:
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error al eliminar {file_path}: {e}")
            print(f"Limpiados {len(ChordRecognitionThread.session_cache_files)} archivos de caché de esta sesión")
            ChordRecognitionThread.session_cache_files = []  # Resetear la lista
    
    def detect_tonality(self, chord_sequence):
        """
        Detecta la posible tonalidad basada en la frecuencia de acordes y aplica reglas de enarmonías
        para usar notaciones más comunes (ej: Gb en lugar de F#)
        """
        # Contador de raíces de acordes
        root_counter = {}
        
        # Contar las apariciones de cada raíz teniendo en cuenta duración
        for start, end, chord in chord_sequence:
            duration = end - start
            root = chord.split(':')[0] if ':' in chord else chord
            if root == 'N':  # Ignorar "No Chord"
                continue
            
            # Obtener solo la raíz sin alteraciones para el conteo
            clean_root = root[0] if len(root) > 0 else ""
            
            if clean_root in root_counter:
                root_counter[clean_root] += duration
            else:
                root_counter[clean_root] = duration
        
        # Encontrar la nota más frecuente (posible tónica)
        if not root_counter:
            return None
            
        tonic_root = max(root_counter, key=root_counter.get)
        
        # Contar las alteraciones para determinar si la tonalidad usa sostenidos o bemoles
        sharps_count = sum(duration for start, end, chord in chord_sequence
                         if '#' in chord.split(':')[0])
        flats_count = sum(duration for start, end, chord in chord_sequence
                         if 'b' in chord.split(':')[0])
        
        # Analizar si hay prevalencia de acordes menores para determinar modo
        minor_count = sum(duration for _, _, chord in chord_sequence 
                         if ':min' in chord or ':m' in chord or (len(chord) > 1 and chord[1] == 'm'))
        major_count = sum(duration for _, _, chord in chord_sequence 
                         if (':maj' in chord or (len(chord) > 0 and ':' not in chord)) 
                         and ':min' not in chord and ':m' not in chord)
        
        mode = 'minor' if minor_count > major_count else 'major'
        
        # Preferir notación con bemoles por ser más común musicalmente
        use_flats = True  # Forzamos el uso de bemoles como preferencia general
        
        # Determinar la alteración correcta para la tónica
        tonic = tonic_root
        for start, end, chord in chord_sequence:
            root = chord.split(':')[0] if ':' in chord else chord
            if root == 'N' or len(root) == 0:
                continue
                
            if root[0] == tonic_root and len(root) > 1:
                # Si encontramos la misma nota raíz pero con alteración, la usamos
                tonic = root
                
                # Aplicamos reglas de enarmonía para usar bemoles
                if '#' in tonic:
                    # Convertir sostenidos a bemoles por ser más comunes
                    enharmonics = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'}
                    if tonic in enharmonics:
                        tonic = enharmonics[tonic]
                break
        
        # Reglas especiales para casos comunes de enarmonías:
        # Preferir Gb sobre F# y Db sobre C# por ser más comunes en notación musical
        if tonic == 'F#':
            tonic = 'Gb'
        elif tonic == 'C#':
            tonic = 'Db'
            
        # Añadir 'm' para tonalidades menores
        if mode == 'minor':
            tonic += 'm'
            
        return {'tonic': tonic, 'mode': mode}
    
    def harmonize_chord(self, chord, tonality):
        """Armoniza un acorde según la tonalidad detectada"""
        if not tonality or ':' not in chord or chord == 'N:N':
            return chord
            
        root, quality = chord.split(':', 1)
        
        # Mapeo de equivalencias enarmónicas
        enharmonics = {
            'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'
        }
        
        # Preferencias de notación según tonalidad
        flat_keys = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 
                     'Dm', 'Gm', 'Cm', 'Fm', 'Bbm', 'Ebm', 'Abm']
        sharp_keys = ['G', 'D', 'A', 'E', 'B', 'F#', 'C#',
                      'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'A#m']
        
        # Preferencias especiales para enarmonías más comunes
        preferred_enharmonics = {
            'F#': 'Gb', 'C#': 'Db', 'D#': 'Eb', 'G#': 'Ab', 'A#': 'Bb'
        }
        
        # Si la raíz está en nuestras preferencias especiales, usamos esa versión
        if root in preferred_enharmonics:
            root = preferred_enharmonics[root]
        # Si no, seguimos las reglas generales según la tonalidad
        elif root in enharmonics:
            tonic = tonality.get('tonic', '')
            # Por defecto, preferimos bemoles en la mayoría de los casos
            if tonic in flat_keys or '#' in root:
                root = enharmonics[root]
        
        return f"{root}:{quality}"
    
    def format_chord_label(self, chord_label, with_extensions=True):
        """Formatea la etiqueta del acorde para incluir séptimas y tensiones"""
        if chord_label == 'N:N':
            return 'N'  # No Chord
            
        if ':' not in chord_label:
            return chord_label
            
        root, quality = chord_label.split(':', 1)
        
        # Siempre mostrar extensiones
        with_extensions = True
        
        # Mapeamos las cualidades de madmom a notación musical estándar más limpia
        quality_map = {
            # Tríadas básicas
            'maj': '',            # Mayor
            'min': 'm',           # Menor
            'dim': 'dim',         # Disminuido
            'aug': 'aug',         # Aumentado
            
            # Séptimas
            'maj7': 'maj7',       # Mayor séptima
            'min7': 'm7',         # Menor séptima
            '7': '7',             # Dominante
            'dim7': 'dim7',       # Disminuido con séptima
            'hdim7': 'm7b5',      # Semidisminuido
            'minmaj7': 'mMaj7',   # Menor con séptima mayor
            
            # Sextas
            'maj6': '6',          # Mayor con sexta
            'min6': 'm6',         # Menor con sexta
            
            # Novenas
            'maj9': 'maj9',       # Mayor con novena
            'min9': 'm9',         # Menor con novena
            '9': '9',             # Dominante con novena
            
            # Tensiones específicas
            'maj7(#11)': 'maj7#11', # Mayor séptima con oncena aumentada
            'maj7(9)': 'maj9',    # Mayor séptima con novena
            '7(b9)': '7b9',       # Dominante con novena bemol
            '7(#9)': '7#9',       # Dominante con novena sostenida
            '7(#11)': '7#11',     # Dominante con oncena aumentada
            '7(13)': '713',       # Dominante con trecena (simplificado)
            '7(b13)': '7b13',     # Dominante con trecena bemol
            
            # Acordes suspendidos
            'sus2': 'sus2',       # Suspendido segunda
            'sus4': 'sus4'        # Suspendido cuarta
        }
        
        # Procesar extensiones especiales con paréntesis
        if '(' in quality and ')' in quality:
            # Extraer la base del acorde y las tensiones
            base_quality = quality[:quality.find('(')]
            tension = quality[quality.find('(')+1:quality.find(')')]
            
            # Formatear la base del acorde
            base_formatted = quality_map.get(base_quality, base_quality)
            
            # Mapa específico para tensiones comunes
            tension_map = {
                '9': '9', 'b9': 'b9', '#9': '#9',
                '11': '11', 'b11': 'b11', '#11': '#11',
                '13': '13', 'b13': 'b13', 
                '6/9': '69' # Caso especial
            }
            
            formatted_tension = tension_map.get(tension, tension)
            
            # Combinar base y tensión de manera más limpia 
            formatted_quality = f"{base_formatted}{formatted_tension}"
        else:
            # Usar el mapa normal
            formatted_quality = quality_map.get(quality, quality)
        
        # Ajustes finales para casos especiales
        if formatted_quality == 'maj7(9)':
            formatted_quality = 'maj9'
        elif formatted_quality == '7(9)':
            formatted_quality = '9'
            
        return f"{root}{formatted_quality}"
    
    def run(self):
        cache_dir = "cache/chord/"
        os.makedirs(cache_dir, exist_ok=True)
        hash_object = hashlib.md5(self.audio_path.encode())
        hashed_filename = hash_object.hexdigest() + ".txt"
        cache_file = os.path.join(cache_dir, hashed_filename)
        
        # Siempre limpiar caché para forzar nuevo análisis de acordes
        if self.clear_cache and os.path.exists(cache_file):
            try:
                os.remove(cache_file)
                print(f"Caché eliminado para: {self.audio_path}")
            except Exception as e:
                print(f"Error al eliminar caché: {e}")
        
        # Verificar si existe un caché para este archivo
        if os.path.exists(cache_file) and not self.clear_cache:
            try:
                # Cargar acordes desde caché
                formatted_chords = []
                with open(cache_file, "r") as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) == 3:
                            start_time, end_time, chord = parts
                            formatted_chords.append((float(start_time), float(end_time), chord))
                
                print(f"Acordes cargados desde caché: {len(formatted_chords)} acordes")
                
                # Registrar este archivo de caché para limpieza al cerrar
                if cache_file not in ChordRecognitionThread.session_cache_files:
                    ChordRecognitionThread.session_cache_files.append(cache_file)
                
                self.result.emit(formatted_chords)
                return
            except Exception as e:
                print(f"Error al cargar caché de acordes: {e}")
                # Continuar con el análisis fresco
        
        # Usar el procesador de características y reconocimiento de acordes
        try:
            # Importamos directamente los procesadores necesarios
            from madmom.features.chords import CNNChordFeatureProcessor, CRFChordRecognitionProcessor
            
            # Desactivamos temporalmente las advertencias para evitar mensajes molestos
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                
                # IMPORTANTE: Configurar el procesador para detectar acordes con extensiones
                feat_processor = CNNChordFeatureProcessor()
                
                # Configuramos el procesador para incluir acordes extendidos 
                # Esto permite detectar séptimas, novenas y otras tensiones
                recog_processor = CRFChordRecognitionProcessor(include_extended_chords=True)
                
                # Extraer características y reconocer acordes
                feats = feat_processor(self.audio_path)
                raw_chords = recog_processor(feats)
                
                # Imprimir los primeros acordes para depuración
                print("\nAcordes reconocidos (sin formatear):")
                for chord in raw_chords[:10]:  # Mostrar los primeros 10 acordes
                    print(f"  {chord[2]}")
                
        except Exception as e:
            print(f"Error en el procesamiento de acordes: {e}")
            # En caso de error, devolvemos una lista vacía
            self.result.emit([])
            return
        
        # Detectar tonalidad basada en los acordes reconocidos
        tonality = self.detect_tonality(raw_chords)
        print(f"Tonalidad detectada: {tonality}")
        
        # Formatear los acordes según la tonalidad detectada
        formatted_chords = []
        with open(cache_file, "w") as f:
            for chord in raw_chords:
                start_time, end_time, chord_label = chord
                
                # Armonizar según tonalidad
                harmonized_chord = self.harmonize_chord(chord_label, tonality)
                
                # Formatear con extensiones (séptimas, tensiones) - MANTENER LAS EXTENSIONES
                final_chord = self.format_chord_label(harmonized_chord, with_extensions=True)
                
                # Imprimir para depuración (solo para acordes que cambian)
                if chord_label != final_chord:
                    print(f"Original: {chord_label} -> Final: {final_chord}")
                
                formatted_chords.append((start_time, end_time, final_chord))
                f.write(f"{start_time},{end_time},{final_chord}\n")
        
        # Registrar este archivo de caché para limpieza al cerrar
        if cache_file not in ChordRecognitionThread.session_cache_files:
            ChordRecognitionThread.session_cache_files.append(cache_file)
        
        # Imprimir los acordes formateados para depuración
        print("\nAcordes formateados (primeros 10):")
        for chord in formatted_chords[:10]:
            print(f"  {chord[2]}")
        
        self.result.emit(formatted_chords)