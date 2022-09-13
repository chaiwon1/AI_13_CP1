from multiprocessing import context
from django.shortcuts import render
from django.conf import settings
import pandas as pd
import joblib
import io
from PIL import Image as im
import torch
import json
import numpy as np
import cv2 as cv

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from .models import ImageModel
from .forms import ImageUploadForm

model = ImageModel
template_name = 'image/imagemodel_form.html'
fields = ["image"]

# main page
def index(request):
    return render(request, 'main/index.html')

# demand predict(VAR model)
def demand(request):
    if request.method == 'GET' :
        return render(request, 'main/demand.html')

    elif request.method == 'POST':
        days = int(request.POST.get('days'))
        counties = request.POST.get('counties')

        if counties == '강남구' :
            # load demand predict models
            gangnamModel = joblib.load('demand_models/model_gangnampickle.pkl')

            # data load
            df_gangnam= pd.read_csv('demand_models/df_gangnam.csv')

            # data preprocessing
            df_gangnam['대여일자'] = df_gangnam['대여일자'].replace('"','')
            df_gangnam = df_gangnam.set_index('대여일자')
            final_diff = df_gangnam.diff().dropna() 

            lagged_values_gangnam = final_diff.values[-6:]

            # forecast result
            result = pd.DataFrame(gangnamModel.forecast(y= lagged_values_gangnam, steps=30), index=final_diff.index[-30:], 
                                    columns=['개포동', '논현동', '대치동', '도곡동', '삼성동', '세곡동', '수서동', '신사동', '압구정동', '양재동','역삼동', '율현동', '일원동', '자곡동', '청담동'])

            a = result.iloc[days-1,:].sort_values(ascending=False)
            do_not_recommend = np.round(a.head(1).values)
            do_not_recommend_where = a.head(1).index[0]
            recommend = np.round(a.tail(1).values)
            recommend_where = a.tail(1).index[0]

            # context = {'counties':counties, 'result':result.to_html}
            context = {'counties': counties, 'result': result, 'days': days,
                        'do_not_recommend': do_not_recommend, 'do_not_recommend_where': do_not_recommend_where, 
                        'recommend':recommend, 'recommend_where': recommend_where}

        elif counties == '송파구' :
            # load demand predict models
            songpaModel=joblib.load('demand_models/model_songpapickle.pkl')
            
            # data load
            df_songpa = pd.read_csv('demand_models/df_songpa.csv')

            # data preprocessing
            df_songpa['대여일자'] = df_songpa['대여일자'].replace('"','')
            df_songpa = df_songpa.set_index('대여일자')
            final_diff = df_songpa.diff().dropna() 

            lagged_values_songpa = final_diff.values[-9:]

            # forecast result
            result = pd.DataFrame(songpaModel.forecast(y= lagged_values_songpa, steps=30), index = final_diff.index[-30:], 
                                    columns=['가락동', '거여동', '마천동', '문정동', '방이동', '삼전동', '석촌동', '송파동', '신천동', '오금동','잠실동', '장지동', '풍납동'])

            a = result.iloc[days-1,:].sort_values(ascending=False)
            do_not_recommend = np.round(a.head(1).values)
            do_not_recommend_where = a.head(1).index[0]
            recommend = np.round(a.tail(1).values)
            recommend_where = a.tail(1).index[0]

            # context = {'counties':counties, 'result':result.to_html}
            context = {'counties': counties, 'result': result, 'days': days,
                        'do_not_recommend': do_not_recommend, 'do_not_recommend_where': do_not_recommend_where, 
                        'recommend':recommend, 'recommend_where': recommend_where}

        else :
            # load demand predict models
            yeongModel=joblib.load('demand_models/model_yeoungpickle.pkl')

            # data load
            df_yeong = pd.read_csv('demand_models/df_yeong.csv')

            # data preprocessing
            df_yeong ['대여일자'] = df_yeong ['대여일자'].replace('"','')
            df_yeong  = df_yeong .set_index('대여일자')
            final_diff = df_yeong .diff().dropna() 

            lagged_values_yeong  = final_diff.values[-4:]

            # forecast result
            result = pd.DataFrame(yeongModel.forecast(y= lagged_values_yeong , steps=30), index = final_diff.index[-30:], columns=['구로동', '당산동', '당산동1가', '당산동2가', '당산동3가', '당산동4가', '당산동5가', '당산동6가',
                                    '대림동', '도림동', '문래동3가', '문래동4가', '문래동5가', '문래동6가', '신길동', '양평동1가',
                                    '양평동2가', '양평동3가', '양평동4가', '양평동5가', '양화동', '여의도동', '영등포동', '영등포동1가',
                                    '영등포동2가', '영등포동4가', '영등포동7가', '영등포동8가'])

            a = result.iloc[days-1,:].sort_values(ascending=False)
            do_not_recommend = np.round(a.head(1).values)
            do_not_recommend_where = a.head(1).index[0]
            recommend = np.round(a.tail(1).values)
            recommend_where = a.tail(1).index[0]

            # context = {'counties':counties, 'result':result.to_html}
            context = {'counties': counties, 'result': result, 'days': days,
                        'do_not_recommend': do_not_recommend, 'do_not_recommend_where': do_not_recommend_where, 
                        'recommend':recommend, 'recommend_where': recommend_where}

        return render(request, 'main/demand.html', context)

# helmet detect model(yolo v5 model)
def helmet(request):
    if request.method == 'GET':
        return render(request, 'main/helmet.html')

    elif request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        img = request.FILES.get('image')
        img_instance = ImageModel(
            image=img
        )
        img_instance.save()

        uploaded_img_qs = ImageModel.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        # resize to (416,416) ; fill in the blanks with black
        image = np.array(img)
        size = (416,416)
        base_pic=np.zeros((size[1],size[0],3),np.uint8)
        h,w=image.shape[:2]
        ash=size[1]/h
        asw=size[0]/w
        if asw<ash:
            sizeas=(int(w*asw),int(h*asw))
        else:
            sizeas=(int(w*ash),int(h*ash))
        image = cv.resize(image,dsize=sizeas)
        base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2),
        int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=image

        # make border ; for detect when pictures are full
        nTop = nBottom = nLeft = nRight = 70
        img = cv.copyMakeBorder(base_pic, nTop, nBottom, nLeft, nRight, 
                            borderType=cv.BORDER_CONSTANT)

        path_hubconfig = "yolov5_code"
        path_weightfile = "best_h.pt"

        model = torch.hub.load(path_hubconfig, 'custom',
                                path=path_weightfile, source='local')

        results = model(img, size=640)

        # save detected img
        results.render()
        for img in results.ims:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out/image_h.jpg", format="JPEG")

        # save confidence score
        results_df = results.pandas().xyxy[0]
        results_df = results_df[results_df['class']==0][['confidence','class']]
        results_json = results_df.to_json(orient="records")
        score = json.loads(results_json)
        final_score = score[0]['confidence']

        file_path = 'media/yolo_out/score_h.json' # score.json path
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(score, file)

        inference_img = "/media/yolo_out/image_h.jpg"

        form = ImageUploadForm()
        context = {
            "form": form,
            "inference_img": inference_img,
            "score": final_score
        }
        return render(request, 'main/helmet.html', context)

# parking detect model(yolo v5 model)
def parking(request):
    if request.method == 'GET' :
        return render(request, 'main/parking.html')

    elif request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        img = request.FILES.get('image')
        img_instance = ImageModel(
            image=img
        )
        img_instance.save()

        uploaded_img_qs = ImageModel.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        # resize to (416,416) ; fill in the blanks with black
        image = np.array(img)
        size = (416,416)
        base_pic=np.zeros((size[1],size[0],3),np.uint8)
        h,w=image.shape[:2]
        ash=size[1]/h
        asw=size[0]/w
        if asw<ash:
            sizeas=(int(w*asw),int(h*asw))
        else:
            sizeas=(int(w*ash),int(h*ash))
        image = cv.resize(image,dsize=sizeas)
        base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2),
        int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=image

        # make border ; for detect when pictures are full
        nTop = nBottom = nLeft = nRight = 70
        img = cv.copyMakeBorder(base_pic, nTop, nBottom, nLeft, nRight, 
                            borderType=cv.BORDER_CONSTANT)

        path_hubconfig = "yolov5_code"
        path_weightfile = "best_p.pt"

        model = torch.hub.load(path_hubconfig, 'custom',
                                path=path_weightfile, source='local')

        results = model(img, size=640)

        # save detected img
        results.render()
        for img in results.ims:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out/image_p.jpg", format="JPEG")

        # save confidence score
        results_df = results.pandas().xyxy[0]
        results_df = results_df[results_df['class']==0][['confidence','class']]
        results_json = results_df.to_json(orient="records")
        score = json.loads(results_json)
        final_score = score[0]['confidence']

        file_path = 'media/yolo_out/score_p.json' # score.json path
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(score, file)

        inference_img = "/media/yolo_out/image_p.jpg"

        form = ImageUploadForm()
        context = {
            "form": form,
            "inference_img": inference_img,
            "score": final_score
        }
        return render(request, 'main/parking.html', context)

def accident(request):
    if request.method == 'GET' :
        return render(request, 'main/accident.html')
    elif request.method == 'POST':
        accident_type = request.POST.get('accident_type')

        if accident_type == str(1) :
            step1 = ' ※ 사고 당시상황 및 사고 현장을 사진을 찍어주세요. (추후 과실비율 산정시 사용될 수 있습니다.'
            step2 = ' ※ 전동킥보드는 도로교통법 제2조 제17호 (가)목, 제21호에 의해 "차"에 해당합니다. 따라서 자동차, 이륜자동차, 원동기장치자전거(전동킥보드)와 교통사고 발생시 조치요령에 따라야 합니다.'
            step3 = [
                    '1. 운전자의 의무',
                    '▶ 연속적인 사고의 방지', 
                    '- 다른 차의 소통에 방해되지 않도록 길 가장자리나 공터 등 안전한 장소에 차를 정차시키고 엔진을 끈다.',
                    '▶ 부상자의 구호',
                    '- 사고현장에 의사, 구급차 등이 도착할 때까지 부상자에게는 가제나 깨끗한 손수건으로 우선 지혈시키는 등 가능한 응급조치를 한다.',
                    '- 이 경우 함부로 부상자를 움직여서는 안 된다. 특히 두부에 상처를 입었을 때에는 움직이지 말아야 한다. 그러나 후속 사고의 우려가 있을 때는 부상자를 안전한 장소로 이동시킨다.',
                    '2. 피해자의 대처 요령',
                    '- 가벼운 상처라도 반드시 경찰공무원에게 알려야 한다. 피해자가 피해신고를 게으르게 하면 후일 사고로 말미암은 후유증의 발생 시 불리하게 될 뿐만 아니라 교통사고증명서를 받을 수 없게 되는 경우가 있다.',
                    '- 가벼운 상처나 외상이 없어도 두부 등에 강한 충격을 받았을 때에는 의사의 진단을 받아 두어야 나중에 후유증이 생겼을 때 선의의 피해를 보지 않는다.'
                    ]
            step4 = '※ 해당 조취를 취한 뒤 고객센터로 접수하세요.' 

            context = {'step1':step1, 'step2':step2, 'step3':step3, 'step4':step4}
            return render(request, 'main/accident.html', context)

        elif accident_type == str(2) :
            step1 = ' ※ 사고 당시상황 및 사고 현장을 사진을 찍어주세요. (추후 과실비율 산정시 사용될 수 있습니다.'
            step2 = ' ※ 전동킥보드는 도로교통법 제2조 제17호 (가)목, 제21호에 의해 "차"에 해당합니다. 따라서 자동차, 이륜자동차, 원동기장치자전거(전동킥보드)와 교통사고 발생시 조치요령에 따라야 합니다.'
        
            step3 = ['1. 전동킥보드 등의 운전으로 인해 사람을 사상하거나 물건을 손괴(이하 “교통사고”라 함)한 경우에는 전동킥보드 등의 운전자는 즉시 정차하여 다음의 조치를 해야 합니다. (「도로교통법」제54조제1항).',
                        '- 사상자를 구호하는 등 필요한 조치',
                        '- 피해자에게 인적 사항(성명·전화번호·주소 등을 말함) 제공',
                        '※ 위 조치를 하지 않은 사람은 5년 이하의 징역이나 1500만원 이하의 벌금에 처해집니다.',
                        '다만, 주·정차된 차만 손괴한 것이 분명한 경우에 피해자에게 인적 사항을 제공하지 않은 사람은 20만원 이하의 벌금이나 구류 또는 과료(科料)에 처해집니다. (「도로교통법」제148조 및 156조제10호)',
                    '2. 경찰에 신고하기',
                    '※ 전동킥보드 등의 운전자는 경찰공무원이 현장에 있을 때에는 그 경찰공무원에게, 경찰공무원이 현장에 없을 때에는 가장 가까운 국가경찰관서(지구대, 파출소 및 출장소를 포함함)에 다음의 사항을 지체 없이 신고해야 합니다.',
                        '하지만, 전동킥보드 등만 손괴된 것이 분명하고 도로에서의 위험방지와 원활한 소통을 위하여 필요한 조치를 한 경우에는 신고하지 않아도 됩니다. (「도로교통법」제54조제2항).',
                        '- 사고가 일어난 곳, 사상자 수 및 부상 정도, 손괴한 물건 및 손괴 정도, 그 밖의 조치사항 등',
                    '※ 사고 발생 시 조치상황 등의 신고를 하지 않은 사람은 30만원 이하의 벌금이나 구류에 처해집니다(「도로교통법」 제154조제4호)',
                    '3. 도주 시 가중처벌',
                        '- 전동킥보드 등의 교통으로 인해 업무상과실·중과실 치사상의 죄(「형법」제268조)를 범한 전동킥보드 등의 운전자(이하 사고운전자 라 함)가 피해자를 구호(救護)하는 등 위의 사상자 구호 등 조치를 하지 않고 도주한 경우에는 가중처벌 됩니다. (「특정범죄 가중처벌 등에 관한 법률」 제5조의3).'
            ]
            step4 = ' ※ 해당 조취를 취한 뒤 고객센터로 접수하세요.'
            
            context = {'step1':step1, 'step2':step2, 'step3':step3, 'step4':step4}
            return render(request, 'main/accident.html', context)

        else :
            step1 = ' 1. 사고 위치, 사고의 원인(원인을 확인할 수 있는 사진 및 현장상황)을 입력하여 주세요.'
            step2 = ' 2. 전동 킥보드의 파손여부를 확인하여 고객센터로 접수하세요. 고객센터 02-oooo-oooo'
            
            context = {'step1':step1, 'step2':step2}
            return render(request, 'main/accident.html', context)