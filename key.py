import os 
import hashlib 
from PyQt5.QtCore import QThread, pyqtSignal
import madmom
import warnings

class KeyRecognitionThread(QThread):
    result = pyqtSignal(str)
    
    def __init__(self, audio_path):
        super().__init__()
        self.audio_path = audio_path
    
    def normalize_key(self, key):
        """
        Normaliza la tonalidad usando enarmonías más comunes
        Convierte F# a Gb, C# a Db, etc. 
        """
        # Preferencias para enarmonías - usamos bemoles (más comunes musicalmente)
        enharmonic_map = {
            'F#': 'Gb', 'C#': 'Db', 'G#': 'Ab', 'D#': 'Eb', 'A#': 'Bb',
            'F# minor': 'Gb minor', 'C# minor': 'Db minor', 'G# minor': 'Ab minor',
            'D# minor': 'Eb minor', 'A# minor': 'Bb minor'
        }
        
        # Si la clave está en nuestro mapa, la reemplazamos
        if key in enharmonic_map:
            return enharmonic_map[key]
            
        return key
    
    def format_key(self, key):
        """
        Da formato a la tonalidad para mostrarla de forma músicalmente correcta
        Ejemplo: Convierte "C# minor" a "C#m" o "Db minor" a "Dbm"
        """
        # Normalizar primero para asegurar que usamos las enarmonías preferidas
        key = self.normalize_key(key)
        
        # Simplificar "minor" a "m"
        if " minor" in key:
            return key.replace(" minor", "m")
        # Si no tiene "minor", es mayor (no se añade nada)
        return key
    
    def run(self):
        cache_dir = "cache/key/"
        os.makedirs(cache_dir, exist_ok=True)
        hash_object = hashlib.md5(self.audio_path.encode())
        hashed_filename = hash_object.hexdigest() + ".txt"
        cache_file = os.path.join(cache_dir, hashed_filename)
        
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cached_key = f.read().strip()
            # Formatear la clave almacenada en caché
            formatted_key = self.format_key(cached_key)
            self.result.emit(formatted_key)
            return
        
        try:
            # Silenciar advertencias temporalmente
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                
                key_processor = madmom.features.key.CNNKeyRecognitionProcessor()
                key_prediction = key_processor(self.audio_path)
                key = madmom.features.key.key_prediction_to_label(key_prediction)
                
                # Guardar en caché la versión original
                with open(cache_file, "w") as f:
                    f.write(key)
                
                # Emitir la versión formateada
                formatted_key = self.format_key(key)
                self.result.emit(formatted_key)
                
        except Exception as e:
            print(f"Error en detección de tonalidad: {e}")
            self.result.emit("Error")