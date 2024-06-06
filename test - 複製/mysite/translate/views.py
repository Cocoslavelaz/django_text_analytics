import os
from django.shortcuts import render
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from datetime import datetime, timedelta


def index(request):
    T_REGION = 'eastus'  # 填入位置/區域
    T_KEY = '73cbc23f369e45e58978d2d9d95b986a'  # 填入金鑰
    T_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'  # 填入文字翻譯的 Web API
    output = ""
    word = ""
    sentiment_localized = ""
    TA_ENDPOINT = 'https://anal.cognitiveservices.azure.com/'  # 情感分析端點
    TA_KEY = 'cc1b6daf528d4644be659995f48ba5cb'  # 情感分析 API 金鑰
    text_analytics_client = TextAnalyticsClient(endpoint=TA_ENDPOINT, credential=AzureKeyCredential(TA_KEY))

    selected_language = "l1"  # 預選"l1"
    download_link = ""

    if request.method == "POST":
        word = request.POST.get('word', None)
        selected_language = request.POST.get('language', "l1")
        text_translator = TextTranslationClient(
            endpoint=T_ENDPOINT,
            credential=TranslatorCredential(T_KEY, T_REGION)
        )
        targets = [InputTextItem(text=word)]
        if selected_language == "l1":
            responses = text_translator.translate(content=targets, to=["zh-hant"], from_parameter="en")
            output = responses[0]["translations"][0]["text"]
        elif selected_language == "l2":
            responses = text_translator.translate(content=targets, to=["en"], from_parameter="zh-hant")
            output = responses[0]["translations"][0]["text"]
        elif selected_language == "l3":
            responses = text_translator.translate(content=targets, to=["zh-hant"], from_parameter="ja")
            output = responses[0]["translations"][0]["text"]
        elif selected_language == "l4":
            responses = text_translator.translate(content=targets, to=["ja"], from_parameter="zh-hant")
            output = responses[0]["translations"][0]["text"]
        
        documents = [output]
        response = text_analytics_client.analyze_sentiment(documents=documents)[0]
        sentiment = f"Sentiment: {response.sentiment}, Positive: {response.confidence_scores.positive:.2f}, Neutral: {response.confidence_scores.neutral:.2f}, Negative: {response.confidence_scores.negative:.2f}"
        def localize_sentiment(sentiment):
            if sentiment == "positive":
                return "正面"
            elif sentiment == "neutral":
                return "中性"
            elif sentiment == "negative":
                return "負面"
            else:
                return sentiment  # 如果情感值不在預期範圍內，返回原始值
        sentiment_localized = localize_sentiment(response.sentiment.lower())  # 將情感值轉換為小寫並本地化

        # 檢查環境變量
        if 'download' in request.POST:
            file_content = f"翻譯結果:\n{output}\n\n情感分析:\n{sentiment}"
            response = HttpResponse(file_content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="translation.txt"'
            return response
    args = {"text": output, "word": word, "sentiment": sentiment_localized,"download_link":download_link}
    return render(request, 'translate/index.html', args)






