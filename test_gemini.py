from google import genai

API_KEY = "AQ.Ab8RN6ISXd2HIvqBiEdgcGWN0EoI0n1ifmV_O2F1GpAn1af1rg"

client = genai.Client(api_key=API_KEY)

try:
    models = client.models.list()

    print("Available Models:")
    for model in models:
        print(model.name)

except Exception as e:
    print(e)