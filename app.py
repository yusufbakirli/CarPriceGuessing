import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns



def main():
    st.sidebar.title('Streamlit ile ML Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa Seçiniz..',["-", "Tahmin Yap", "İstatistik Görüntüle"])
    
    if selected_page == "-":
        st.title('Araba Fiyatı Tahmin Uygulamasına Hoşgeldiniz')
    
        st.markdown(
            """
            Bu proje makine öğrenmesi uygulamalarının web ortamında streamlit kullanılarak yayınlanmasına örnek olarak geliştirilmiştir. 
            Bir e-ticaret sitesi üzerinden 1000 adet araba verileri çekilmiş ve incelenmiştir. Bu veriler kullanılarak makine öğrenmesi
            modelleri eğitilmiş ve projeye dahil edilmiştir.
            """)
        
        st.info("Tahmin yapmak, istatistikleri görüntülemek ve proje hakkında daha fazla bilgi edinmek için sol tarafta bulunan menüyü kullanınız.")
        
    if selected_page == "Tahmin Yap":
        predict()
        
    if selected_page == "İstatistik Görüntüle":
        eda()

def eda():
    st.title('İstatistikler')
    
    data = pd.read_excel("C:/Users/Yusuf/Desktop/proje/machine learning/cars_to_presentation.xlsx")
    
    st.header("Bütün veriler")
    st.dataframe (data)
    
    plt.figure(figsize=(16,16))
    plt.subplot(2,1,1)
    sns.countplot(x='Marka', data = data, order = data['Marka'].value_counts().index)
    plt.xticks(rotation = 90)
    plt.xlabel("Marka Adı")
    plt.ylabel("Ürün Sayısı")
    st.header("Ürün Sayısına Göre Markaların Sıralaması")
    st.pyplot(fig=plt)
    
    plt.figure(figsize=(16,16))
    plt.subplot(2,1,1)
    sns.countplot(x='Kasa_Tipi', data = data, order = data['Kasa_Tipi'].value_counts().index)
    plt.xlabel("Kasa Tipi")
    plt.ylabel("Ürün Sayısı")
    plt.xticks(rotation = 90)
    st.header("Ürün Sayısına Göre Kasa Tipleri")
    st.pyplot(fig=plt)
    
    plt.figure(figsize=(16,16))
    plt.subplot(2,1,1)
    sns.countplot(x='Vites_Tipi', data = data, order = data['Vites_Tipi'].value_counts().index)
    plt.xlabel("Vites Tipi")
    plt.ylabel("Ürün Sayısı")
    plt.xticks(rotation = 90)
    st.header("Ürün Sayısına Göre Vites Tipleri")
    st.pyplot(fig=plt)
    
    plt.figure(figsize=(16,16))
    plt.subplot(2,1,1)
    sns.countplot(x='Yakit_Tipi', data = data, order = data['Yakit_Tipi'].value_counts().index)
    plt.xlabel("Yakıt Tipi")
    plt.ylabel("Ürün Sayısı")
    plt.xticks(rotation = 90)
    st.header("Ürün Sayısına Göre Yakıt Tipleri")
    st.pyplot(fig=plt)
    
    
def predict():
    # Markalar ve Modellerin yüklenmesi 
    markalar = load_data()

    # Kullanıcı arayüzü ve değer alma
    st.title('Merhaba, *Streamlit!*')
    selected_brand= marka_index(markalar, st.selectbox ('Marka Seçiniz..', markalar))

    selected_ct = kasa_tipi (st.radio("Kasa Tipi", ('Sedan', 'Hatchback', 'Coupe', 'Station wagon', 'MPV')))

    selected_gt = vites_tipi (st.radio("Vites Tipi", ('Düz', 'Otomatik', 'Yarı Otomatik')))

    selected_ft = yakit_tipi (st.radio("Yakıt Tipi", ('Dizel', 'Benzin', 'LPG & Benzin', 'Hibrit')))

    selected_problem = st.number_input("Boya-Değişen",min_value=0,max_value=14) 
    st.write("Boya-Değişen: "+str(selected_problem)+" tane")
    
    selected_km = st.number_input("Kilometre",min_value=0,max_value=1000000) 
    st.write("Kilometre: "+str(selected_km)+" km")
    
    selected_hp = st.number_input("Motor Gücü",min_value=50,max_value=600) 
    st.write("Motor Gücü: "+str(selected_hp)+" hp")
    
    selected_year = st.number_input("Yıl",min_value=1986,max_value=2023) 
    st.write("Yıl: "+str(selected_year))
    
    
    selected_model = st.selectbox('Tahmin Modeli Seçiniz..',["Decision Tree", "Multiple Linear", "Random Forest", "Gradient Boosting"])

    prediction_value = create_prediction_value (selected_brand, selected_ct, selected_gt, selected_ft, selected_problem, selected_km, selected_hp, selected_year)
    prediction_model = load_models (selected_model)

    if st.button("Tahmin Yap"):
        result = predict_models (prediction_model, prediction_value)
        if result != None:
            st.success('Tahmin Başarılı')
            st.balloons()
            st.write("Tahmin Edilen Fiyat: "+ result + " TL")
        else:
            st.error('Tahmin yaparken hata meydana geldi..!')


def load_data():
    markalar = pd.read_excel("C:/Users/Yusuf/Desktop/proje/machine learning/marka.xlsx") 
    return markalar

def load_models (modelName):
    if modelName == "Decision Tree":
        dt_model = joblib.load("C:/Users/Yusuf/Desktop/proje/machine learning/cars_decision_tree_model.pkl")
        return dt_model
    
    elif modelName == "Multiple Linear":
        ml_model = joblib.load("C:/Users/Yusuf/Desktop/proje/machine learning/cars_multiple_linear_model.pkl") 
        return ml_model
    
    elif modelName == "Random Forest":
        rf_model = joblib.load("C:/Users/Yusuf/Desktop/proje/machine learning/cars_random_forest_model.pkl") 
        return rf_model
    
    elif modelName == "Gradient Boosting":
        gb_model = joblib.load("C:/Users/Yusuf/Desktop/proje/machine learning/cars_gradient_boosting_model.pkl") 
        return gb_model

    else:
        st.write("Model yüklenirken hata meydana geldi..!") 
        return 0

def marka_index(markalar,marka):
    index = int(markalar[markalar["Marka"]==marka].index.values) 
    return index

def yakit_tipi(yakit_tipi):
    if yakit_tipi == "Benzin":
        return 0
    elif yakit_tipi == "Dizel":
        return 1
    elif yakit_tipi == "Hibrit":
        return 2
    else:
        return 3
    
def kasa_tipi(kasa_tipi):
    if kasa_tipi == "Coupe":
        return 0
    elif kasa_tipi == "Hatchback":
        return 1
    elif kasa_tipi == "MPV":
        return 2
    elif kasa_tipi == "Sedan":
        return 3
    else:
        return 4
    
def vites_tipi(vites_tipi):
    if vites_tipi == "Düz":
        return 0
    elif vites_tipi == "Otomatik":
        return 1
    else:
        return 2

def create_prediction_value(marka, kasa_tipi, vites_tipi, yakit_tipi, boya_degisen, kilometre, motor_gucu, yil):
    res = pd.DataFrame(data = 
             {'Marka':[marka],'Kasa_Tipi':[kasa_tipi],'Vites_Tipi':[vites_tipi],
              'Yakit_Tipi':[yakit_tipi],'Boya_Degisen':[boya_degisen],'Kilometre':[kilometre],
              'Motor_Gucu':[motor_gucu],'Yil':[yil]})
    return res

def predict_models (model, res):
    result = str(int (model.predict(res))).strip('[]')
    return result


if __name__ == "__main__":
    main()