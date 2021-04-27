from flask import Flask, render_template
from forms import PredictForm
import requests
import json

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key'

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()

    if form.submit():

        # Replace the following key with the IAM Key that you have generated.
        iamkey = 'YOUR IAM KEY GOES HERE'
        deployment_id = 'YOUR DEPLOYMENT ID GOES HERE'

        iam_token_response =  requests.post('https://iam.cloud.ibm.com/oidc/token', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': iamkey})
        iam_token_response_json = json.loads(iam_token_response.text)
        iam_token = iam_token_response_json["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+iam_token}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [int(form.pregnancies.data), int(form.glucose.data), int(form.bloodpressure.data),
            int(form.skinthickness.data), int(form.insulin.data), float(form.bmi.data), float(form.diabetespedigreefunction.data),
            int(form.age.data)]

        userInput = []
        userInput.append(python_object)

        payload_json = {"input_data": [{"fields": ["Pregnancies", "Glucose", "BloodPressure",
          "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"], "values": userInput }]}

        response_scoring = requests.post(f"https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/{deployment_id}/predictions?version=2021-04-23", json=payload_json, headers=header)

        output = json.loads(response_scoring.text)

        for key in output:
          opt = output[key]

        for key in opt[0]:
          bc = opt[0][key]

        roundedResult = round(bc[0][0],2)

        if roundedResult == 1:
          msg = "Positive - Susceptible to Diabetes"
        else:
          msg = "Negative - Not Susceptible to Diabetes"

        form.outcome = msg
        return render_template('index.html', form=form)

if __name__ == "__main__":
  app.run(threaded=True, port = int(os.environ.get('PORT', 5000)))