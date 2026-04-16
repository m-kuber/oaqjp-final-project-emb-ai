import urllib.request
import json

def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    data = json.dumps({
        "raw_document": {
            "text": text_to_analyze
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        response = urllib.request.urlopen(req)
        
        # ✅ Check status code
        if response.getcode() == 400:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }
        
        response_text = response.read().decode("utf-8")
        response_dict = json.loads(response_text)
        
        emotions = response_dict["emotionPredictions"][0]["emotion"]
        
        dominant_emotion = max(emotions, key=emotions.get)
        
        return {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"],
            "dominant_emotion": dominant_emotion
        }

    except:
        # Handles blank input / bad request
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }