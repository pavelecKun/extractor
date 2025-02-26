import os
import hashlib
import warnings
from PyQt5.QtCore import QThread, pyqtSignal
import madmom

class TempoDetectionThread(QThread):
    result = pyqtSignal(int)

    def __init__(self, audio_file_path):
        super().__init__()
        self.audio_file_path = audio_file_path

    def run(self):
        cache_dir = "cache/tempo/"
        os.makedirs(cache_dir, exist_ok=True)
        hash_object = hashlib.md5(self.audio_file_path.encode())
        hashed_filename = hash_object.hexdigest() + ".txt"
        cache_file = os.path.join(cache_dir, hashed_filename)

        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cached_tempo = int(f.read().strip())
            self.result.emit(cached_tempo)
            return

        # Silenciar advertencias durante el procesamiento
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            
            try:
                # Usando las clases correctas disponibles en madmom
                from madmom.features.beats import RNNBeatProcessor
                from madmom.features.tempo import TempoEstimationProcessor
                
                # Extraer beats usando RNNBeatProcessor
                proc = RNNBeatProcessor()
                act = proc(self.audio_file_path)
                
                # Estimar tempo usando TempoEstimationProcessor (¡no TempoDetectionProcessor!)
                tempo_proc = TempoEstimationProcessor(fps=100)
                tempos = tempo_proc(act)
                
                if len(tempos) > 0:
                    # El formato de salida es una lista de tempos con sus probabilidades
                    # [(tempo1, prob1), (tempo2, prob2), ...]
                    top_tempo = tempos[0][0]  # Tomamos el primer tempo (más probable)
                    adjusted_tempo = self.adjust_tempo(top_tempo)
                    
                    with open(cache_file, "w") as f:
                        f.write(str(round(adjusted_tempo)))
                    
                    self.result.emit(round(adjusted_tempo))
                else:
                    # Alternativa: Usar DBNTempoDetectionProcessor si no funcionó el anterior
                    from madmom.features.tempo import DBNTempoDetectionProcessor
                    
                    tempo_dbn = DBNTempoDetectionProcessor(fps=100)
                    tempos = tempo_dbn(act)
                    
                    if len(tempos) > 0:
                        top_tempo = tempos[0]
                        adjusted_tempo = self.adjust_tempo(top_tempo)
                        
                        with open(cache_file, "w") as f:
                            f.write(str(round(adjusted_tempo)))
                        
                        self.result.emit(round(adjusted_tempo))
                    else:
                        self.result.emit(120)  # Valor por defecto si todo falla
                    
            except Exception as e:
                print(f"Error detectando tempo: {e}")
                try:
                    # Plan de respaldo: Usar otra técnica si la primera falló
                    from madmom.features.tempo import ACFTempoDetectionProcessor
                    from madmom.features.beats import RNNBeatProcessor
                    
                    proc = RNNBeatProcessor()
                    act = proc(self.audio_file_path)
                    
                    # Usar procesador de autocorrelación como alternativa
                    tempo_acf = ACFTempoDetectionProcessor(fps=100)
                    tempos = tempo_acf(act)
                    
                    if len(tempos) > 0:
                        top_tempo = tempos[0]
                        adjusted_tempo = self.adjust_tempo(top_tempo)
                        
                        with open(cache_file, "w") as f:
                            f.write(str(round(adjusted_tempo)))
                        
                        self.result.emit(round(adjusted_tempo))
                    else:
                        self.result.emit(120)  # Valor por defecto
                        
                except Exception as e2:
                    print(f"Error en método alternativo: {e2}")
                    self.result.emit(120)  # Valor por defecto

    def adjust_tempo(self, tempo):
        """Ajusta el tempo para que esté en un rango razonable (70-190 BPM)"""
        while tempo < 70:
            tempo *= 2
        while tempo > 190:
            tempo /= 2
        return tempo