from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DecimalField

class PredictForm(FlaskForm):
   pregnancies = IntegerField('Number of Pregnancies')
   glucose = IntegerField('Blood Glucose Level')
   bloodpressure = IntegerField('Blood pressure (mm Hg)')
   skinthickness = IntegerField('Skin Thickness (mm)')
   insulin = IntegerField('Serum Insulin (mu U/ml)')
   bmi = DecimalField('BMI')
   diabetespedigreefunction = DecimalField('Diabetes Pedigree Function')
   age = IntegerField('Age (years)')
   submit = SubmitField('Predict')
   abc = "" # this variable is used to send information back to the front page
