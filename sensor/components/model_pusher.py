from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
import os,sys
from sensor.ml.metric.classification_metric import get_classification_metric
from sensor.utils.main_utils import save_object, load_object,write_yaml_file
from sensor.ml.model.estimator import ModelResolver
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping
import shutil

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.model_evaluation_artifact=model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_pusher(self)->ModelPusherArtifact:

        trained_model_path = self.model_evaluation_artifact.trained_model_path

        #Creating model pusher dir to save model
        model_file_path=self.model_pusher_config.model_file_path
        os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
        shutil.copy(src=trained_model_path, dst=model_file_path)

        saved_model_path=self.model_pusher_config.saved_model_path
        os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
        shutil.copy(src=trained_model_path, dst=saved_model_path)

        model_pusher_artifact=ModelPusherArtifact(saved_model_path=saved_model_path,model_file_path=model_file_path)
        logging.info(f"model pusher artifact: {model_pusher_artifact}")
        return model_pusher_artifact


        



