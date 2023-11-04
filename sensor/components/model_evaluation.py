
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig
import os,sys
from sensor.ml.metric.classification_metric import get_classification_metric
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object,write_yaml_file
from sensor.ml.model.estimator import ModelResolver
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping
import pandas  as  pd

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                 data_validation_artifact:DataValidationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:

        valid_train_file_path = self.data_validation_artifact.valid_train_file_path
        valid_test_file_path = self.data_validation_artifact.valid_test_file_path

        train_df = pd.read_csv(valid_train_file_path)
        test_df= pd.read_csv(valid_test_file_path)

        df = pd.concat([train_df,test_df])
        y_true = df[TARGET_COLUMN]
        y_true.replace(TargetValueMapping().to_dict(),inplace=True)
        df.drop(TARGET_COLUMN,axis=1,inplace=True)

        trained_model_file_path = self.model_trainer_artifact.trained_model_file_path

        model_resolver = ModelResolver()
        
        is_model_accepted=True
        if not model_resolver.is_model_exists():
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=None,
                best_model_path=None,
                trained_model_path=trained_model_file_path,
                trained_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                best_model_metric_artifact=None)
            
            logging.info(f"model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        
        #load LATEST MODEL AND TRAINED MODEL
        latest_model_file_path = model_resolver.get_best_model_file_path()
        latest_model = load_object(file_path=latest_model_file_path)
        trained_model = load_object(file_path=trained_model_file_path)

        #PREDICTION
        
        y_train_pred = trained_model.predict(df)
        y_latest_pred = latest_model.predict(df)

        #METRIC
        train_metric = get_classification_metric(y_true=y_true,y_pred=y_train_pred)
        latest_metric = get_classification_metric(y_true=y_true,y_pred=y_latest_pred)

        improved_accuracy=train_metric.f1_score-latest_metric.f1_score

        if self.model_evaluation_config.chanage_threshold_score<improved_accuracy:
            #0.02<0.03
            is_model_accepted=True
        else:
            is_model_accepted=False

        model_evaluation_artifact=ModelEvaluationArtifact(
            is_model_accepted=is_model_accepted,
            improved_accuracy=improved_accuracy,
            best_model_path=latest_model_file_path,
            trained_model_path=trained_model_file_path,
            trained_model_metric_artifact=train_metric,
            best_model_metric_artifact=latest_metric)
        

        model_evaluation_report = model_evaluation_artifact.__dict__

        #save the report
        write_yaml_file(self.model_evaluation_config.report_file_name,model_evaluation_report)

        logging.info(f"model evaluation artifact: {model_evaluation_artifact}")
        return model_evaluation_artifact



        

