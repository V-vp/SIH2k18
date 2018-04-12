from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Panchayat, RankedPanchayat, villageDetails
import pandas as pd
import numpy as np

from django.conf import settings
import random
import string
import pickle
import _pickle
import pandas as pd
from sklearn.naive_bayes import GaussianNB
cs = settings.CSV

def index(request):
    template='gaa/home.html'

    return render(request,template)


def list(request):

    df = pd.read_csv(cs)

    district = df.District
    taluk = df.Taluk
    gram_panchayat = df.Grampanchayat
    stdofliving = df.Standardoflivingindex
    health = df.Healthindex
    education = df.Educationindex
    hdi = df.HDI

    n_points = 999

    village_info = [[districtz, talukz, gram_panchayatz] for districtz, talukz, gram_panchayatz in
                    zip(district, taluk, gram_panchayat)]
    village_number = [[stdoflivingz, healthz, educationz, hdiz] for stdoflivingz, healthz, educationz, hdiz in
                      zip(stdofliving, health, education, hdi)]

    avg_stdofliving = np.sum(stdofliving) / n_points
    avg_health = np.sum(health) / n_points
    avg_education = np.sum(education) / n_points
    avg_hdi = np.sum(hdi) / n_points

    Y = [0] * n_points

    for i in range(0, n_points):
        count = 0
        if stdofliving[i] < avg_stdofliving:
            count = count + 1
        if health[i] < avg_health:
            count = count + 1
        if education[i] < avg_education:
            count = count + 1
        if hdi[i] < avg_hdi:
            count = count + 1
        if count >= 2:
            Y[i] = 1

    print(np.sum(Y))

    X_train = village_number[:750]
    X_test = village_number[750:]
    Y_train = Y[:750]
    Y_test = Y[750:]

    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    from time import time
    t0 = time()
    clf.fit(X_train, Y_train)
    print("Classification training time:", round(time() - t0, 3), "s")
    pred = clf.predict(X_test)
    # print(pred)
    prob = clf.predict_proba(X_test)
    # print(prob)
    from sklearn.metrics import accuracy_score
    print("Accuracy of Program: ", accuracy_score(pred, Y_test) * 100, "%")

    # print (hdi)
    probability = []
    for i in range(0, 249):
        ss = (1-prob[i][1])*100
        probability.append(ss)

    #print(final_list)
    rank_list = []
    for i in range(0, 249):
        rank_list.append(i+1)

    final_list = [[probab, gram,ran] for probab,gram,ran in zip(probability, gram_panchayat,rank_list)]
    final_list.sort()

    for i in range(0, 249):
        final_list[i][2] = i+1


    #for ii in range(0,249):
        #final_list[ii][0] final_list[ii][1] final_list[ii][2]


    page = request.GET.get('page', 1)

    paginator = Paginator(final_list, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request,'gaa/index.html',{'users': users , 'panchayat': panchayat,})

def panchayat_details(request):

    df = pd.read_csv(cs)
    district = df.District
    taluk = df.Taluk
    gram_panchayat = df.Grampanchayat
    stdofliving = df.Standardoflivingindex
    health = df.Healthindex
    education = df.Educationindex
    hdi = df.HDI

    n_points = 999

    village_info = [[districtz, talukz, gram_panchayatz] for districtz, talukz, gram_panchayatz in
                    zip(district, taluk, gram_panchayat)]
    village_number = [[stdoflivingz, healthz, educationz, hdiz] for stdoflivingz, healthz, educationz, hdiz in
                      zip(stdofliving, health, education, hdi)]

    village250 = [[districtz, talukz, gram_panchayatz,stdoflivingz, healthz, educationz, hdiz] for districtz, talukz, gram_panchayatz,stdoflivingz, healthz, educationz, hdiz in
                    zip(district, taluk, gram_panchayat,stdofliving, health, education, hdi)]





    for ii in range(0, 999):

        panchayat = Panchayat()
        panchayat.panchayat = village250[ii][2]
        panchayat.district = village250[ii][0]
        panchayat.taluka = village250[ii][1]
        panchayat.stdofliving = village250[ii][3]
        panchayat.health = village250[ii][4]
        panchayat.education = village250[ii][5]
        panchayat.hdi = village250[ii][6]
        panchayat.save()

    return render(request, 'gaa/index.html')

def ranked_panchayats(request):

    df = pd.read_csv(cs)
    district = df.District
    taluk = df.Taluk
    gram_panchayat = df.Grampanchayat
    stdofliving = df.Standardoflivingindex
    health = df.Healthindex
    education = df.Educationindex
    hdi = df.HDI

    n_points = 999

    village_info = [[districtz, talukz, gram_panchayatz] for districtz, talukz, gram_panchayatz in
                    zip(district, taluk, gram_panchayat)]
    village_number = [[stdoflivingz, healthz, educationz, hdiz] for stdoflivingz, healthz, educationz, hdiz in
                      zip(stdofliving, health, education, hdi)]

    village = [[districtz, talukz, gram_panchayatz,stdoflivingz, healthz, educationz, hdiz] for districtz, talukz, gram_panchayatz,stdoflivingz, healthz, educationz, hdiz in
                    zip(district, taluk, gram_panchayat,stdofliving, health, education, hdi)]


    avg_stdofliving = np.sum(stdofliving) / n_points
    avg_health = np.sum(health) / n_points
    avg_education = np.sum(education) / n_points
    avg_hdi = np.sum(hdi) / n_points

    Y = [0] * n_points

    for i in range(0, n_points):
        count = 0
        if stdofliving[i] < avg_stdofliving:
            count = count + 1
        if health[i] < avg_health:
            count = count + 1
        if education[i] < avg_education:
            count = count + 1
        if hdi[i] < avg_hdi:
            count = count + 1
        if count >= 2:
            Y[i] = 1

    print(np.sum(Y))

    X_train = village_number[:750]
    X_test = village_number[750:]
    Y_train = Y[:750]
    Y_test = Y[750:]

    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    from time import time
    t0 = time()
    clf.fit(X_train, Y_train)
    print("Classification training time:", round(time() - t0, 3), "s")
    pred = clf.predict(X_test)
    # print(pred)
    prob = clf.predict_proba(X_test)
    # print(prob)
    from sklearn.metrics import accuracy_score
    print("Accuracy of Program: ", accuracy_score(pred, Y_test) * 100, "%")

    # print (hdi)
    probability = []
    for i in range(0, 249):
        ss = (1 - prob[i][1]) * 100
        probability.append(ss)

    # print(final_list)
    rank_list = []
    for i in range(0, 249):
        rank_list.append(i + 1)

    final_list = [[probab, gram, ran] for probab, gram, ran in zip(probability, gram_panchayat, rank_list)]
    final_list.sort()

    RankedPanchayat.objects.all().delete()

    for ii in range(0, 249):

        panchayat = RankedPanchayat()
        panchayat.panchayat = final_list[ii][1]
        panchayat.dev_index = final_list[ii][0]
        panchayat.rank = ii + 1
        panchayat.save()

    return render(request, 'gaa/index.html')

@login_required
def panchayat_list(request):
    panchayats = RankedPanchayat.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(panchayats, 10)

    try:
        panchayats = paginator.page(page)
    except PageNotAnInteger:
        panchayats = paginator.page(1)
    except EmptyPage:
        panchayats = paginator.page(paginator.num_pages)
    return render(request, 'gaa/panchayat_list.html', {'panchayats': panchayats,})


def panchayat(request, pk):

    panchayat = get_object_or_404(RankedPanchayat, pk=pk)
    panchayat_details = Panchayat.objects.get(panchayat = panchayat.panchayat)

    return render(request, 'gaa/village_info.html', {'panchayat': panchayat , 'panchayat_details' : panchayat_details})

'''def vd(request):


    df = pd.read_csv(cs)
    district = df.District
    taluk = df.Taluk
    gram_panchayat = df.Grampanchayat
    stdofliving = df.Standardoflivingindex
    health = df.Healthindex
    education = df.Educationindex
    hdi = df.HDI

    n_points = 999

    village_info = [[districtz, talukz, gram_panchayatz] for districtz, talukz, gram_panchayatz in
                    zip(district, taluk, gram_panchayat)]
    village_number = [[stdoflivingz, healthz, educationz, hdiz] for stdoflivingz, healthz, educationz, hdiz in
                      zip(stdofliving, health, education, hdi)]

    village = [[districtz, talukz, gram_panchayatz,stdoflivingz, healthz, educationz, hdiz] for districtz, talukz, gram_panchayatz,stdoflivingz, healthz, educationz, hdiz in
                    zip(district, taluk, gram_panchayat,stdofliving, health, education, hdi)]


    avg_stdofliving = np.sum(stdofliving) / n_points
    avg_health = np.sum(health) / n_points
    avg_education = np.sum(education) / n_points
    avg_hdi = np.sum(hdi) / n_points

    Y = [0] * n_points

    for i in range(0, n_points):
        count = 0
        if stdofliving[i] < avg_stdofliving:
            count = count + 1
        if health[i] < avg_health:
            count = count + 1
        if education[i] < avg_education:
            count = count + 1
        if hdi[i] < avg_hdi:
            count = count + 1
        if count >= 2:
            Y[i] = 1

    print(np.sum(Y))

    X_train = village_number[:750]
    X_test = village_number[750:]
    Y_train = Y[:750]
    Y_test = Y[750:]

    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    from time import time
    t0 = time()
    clf.fit(X_train, Y_train)
    print("Classification training time:", round(time() - t0, 3), "s")
    pred = clf.predict(X_test)
    # print(pred)
    prob = clf.predict_proba(X_test)
    # print(prob)
    from sklearn.metrics import accuracy_score
    print("Accuracy of Program: ", accuracy_score(pred, Y_test) * 100, "%")

    # print (hdi)
    probability = []
    for i in range(0, 249):
        ss = (1 - prob[i][1]) * 100
        probability.append(ss)

    # print(final_list)
    rank_list = []
    for i in range(0, 249):
        rank_list.append(i + 1)

    final_list = [[probab, gram, ran] for probab, gram, ran in zip(probability, gram_panchayat, rank_list)]
    final_list.sort()



    description = [
            "According to Census 2011 information the location code or village code of Maninalkur village is 617553. Maninalkur village is located in Bantval Tehsil of Dakshina Kannada district in Karnataka, India. It is situated 26km away from sub-district headquarter Bantval and 50km away from district headquarter Mangalore. As per 2009 stats, Maninalkur village is also a gram panchayat.The total geographical area of village is 1365.46 hectares. Maninalkur has a total population of 5,106 peoples. There are about 983 houses in Maninalkur village. Bantval is nearest town to Maninalkur which is approximately 16km away.",
            "According to Census 2011 information the location code or village code of Rayee village is 617529. Rayee village is located in Bantval Tehsil of Dakshina Kannada district in Karnataka, India. It is situated 10km away from sub-district headquarter Bantval and 30km away from district headquarter Mangalore. As per 2009 stats, Rayee village is also a gram panchayat. The total geographical area of village is 683.26 hectares. Rayee has a total population of 2,012 peoples. There are about 416 houses in Rayee village. Bantval is nearest town to Rayee which is approximately 10km away.",
            "According to Census 2011 information the location code or village code of Nimbegondi village is 87729. Nimbegondi village is located in gud Tehsil of Dakshina Kannada district in Tamilnadu, India. It is situated 10km away from sub-district headquarter fantval and 40km away from district headquarter Bangalore. As per 2009 stats, Nimbegondi village is also a gram panchayat. The total geographical area of village is 683.26 hectares. Nimbegondi has a total population of 2,012 peoples. There are about 416 houses in Nimbegondi village. Bantval is nearest town to Nimbegondi which is approximately 10km away.",
            "According to Census 2011 information the location code or village code of Shanthipura village is 608764. Shanthipura village is located in Udupi Tehsil of Udupi district in Karnataka, India. It is situated 25km away from Udupi, which is both district & sub-district headquarter of Kodi village. As per 2009 stats, Kodi village is also a gram panchayat.The total geographical area of village is 442.07 hectares. Shanthipura has a total population of 4,490 peoples. There are about 860 houses in Kodi village. Saligram is nearest town to Shanthipura which is approximately 3km away.",
            "According to Census 2011 information the location code or village code of Panja village is 617445. Panja village is located in Mangalore Tehsil of Dakshina Kannada district in Karnataka, India. It is situated 30km away from Mangalore, which is both district & sub-district headquarter of Panja village. As per 2009 stats, Kemral is the gram panchayat of Panja village.The total geographical area of village is 152.84 hectares. Panja has a total population of 418 peoples. There are about 99 houses in Panja village. Mulki is nearest town to Panja which is approximately 16km away.",
            "Ghadsai is a Village in Karwar Taluk in Uttar Kannad District of Karnataka State, India. It belongs to Belgaum Division . It is located 8 KM towards North from District head quarters Karwar. 497 KM from State capital Bangalore Ghadsai is surrounded by Uttar Kannad Taluk towards South , Canacona Taluk towards North , Ankola Taluk towards South , Quepem Taluk towards North . Karwar , Curchorem Cacora , Madgaon , Margao are the near by Cities to Ghadsai. It is near to arabian sea. There is a chance of humidity in the weather.",
            " According to Census 2011 information the location code or village code of Mala village is 608887. Mala village is located in Karkal Tehsil of Udupi district in Karnataka, India. It is situated 20km away from sub-district headquarter Karkala and 53km away from district headquarter Udupi. As per 2009 stats, Mala village is also a gram panchayat.The total geographical area of village is 4700.44 hectares. Mala has a total population of 5,998 peoples. There are about 1,338 houses in Mala village. Karkal is nearest town to Mala which is approximately 20km away.",
            "According to Census 2011 information the location code or village code of Hoddur village is 617836. Hoddur village is located in Madikeri Tehsil of Kodagu district in Karnataka, India. It is situated 18km away from Madikeri, which is both district & sub-district headquarter of Hoddur village. As per 2009 stats, Hoddur village is also a gram panchayat.The total geographical area of village is 950.53 hectares. Hoddur has a total population of 2,761 peoples. There are about 725 houses in Hoddur village. Madikeri is nearest town to Hoddur which is approximately 18km away.",
            "According to Census 2011 information the location code or village code of Sovinkoppa village is 603629. Sovinkoppa village is located in Siddapur Tehsil of Uttara Kannada district in Karnataka, India. It is situated 24km away from sub-district headquarter Siddapur and 131km away from district headquarter Karwar. As per 2009 stats, Sovinkoppa village is also a gram panchayat.The total geographical area of village is 415.7 hectares. Sovinkoppa has a total population of 546 peoples. There are about 136 houses in Sovinkoppa village. Siddapur is nearest town to Sovinkoppa which is approximately 24km away.",
            "Bidaluru is a Village in Devanhalli Taluk in Bangalore Rural District of Karnataka State, India. It belongs to Bangalore Division . It is located 5 KM towards North from District head quarters Bangalore. 5 KM from Devanhalli. 41 KM from State capital Bangalore. Bidaluru Pin code is 562110 and postal head office is Devanahallifort. This Place is in the border of the Bangalore Rural District and Chikballapur District. Chikballapur District Chikballapur is North towards this place ."
            ]
    X = [12.867705, 12.976048, 14.06018, 14.189020, 12.671889, 14.897320, 10.247651, 12.314958, 14.395584, 13.279019]
    Y = [75.147216, 75.046535, 75.736271, 75.897618, 75.476361, 74.238622, 76.275693, 75.709469, 74.777893, 77.68766]

    for ii in range(9, 10):

        panchayat = villageDetails()
        panchayat.panchayat = final_list[ii][1]
        panchayat.description = description[ii]
        panchayat.xcor = X[ii]
        panchayat.ycor = Y[ii]
        panchayat.save()
    return render(request, 'gaa/index.html')'''
