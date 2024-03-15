import streamlit as st
import pandas as pd
from pymongo import MongoClient

def main():
    st.markdown("<h1 style='text-align: center; color: #203ca4; font-size:50px;'>Venhancer Memnuniyet Anketi</h1>", unsafe_allow_html=True)
    
    
    st.markdown("<p style='font-family: Arial; font-size: 25px;'>Aşağıdakilerden ne kadar memnunsunuz?</p>", unsafe_allow_html=True)
                 
               

    sorular = [
        
        "Soru1 : Şirkette genel olarak ne kadar memnunsunuz?",
        "Soru2 : Yaptığınız işten ne kadar memnunsunuz?",
        "Soru3 : Yöneticinizden ne kadar memnunsunuz?",
        "Soru4 : İş arkadaşlarınızla ilişkilerinizden ne kadar memnunsunuz?",
        "Soru5 : Şirketin çalışma ortamından ne kadar memnunsunuz?",
        "Soru6 : Şirketin size sağladığı maaş ve yan haklardan ne kadar memnunsunuz?",
        "Soru7 : Şirketin kariyer geliştirme imkanları hakkında ne düşünüyorsunuz?",
        "Soru8 : Şirketin iletişim politikasından ne kadar memnunsunuz?"
    ]
    
    

    cevaplar = {}
    
    

    for soru in sorular:
        secenekler = ["Seçilmedi", "Memnun", "Nötr", "Memnun Değil"]
        formatted_soru = f"{soru}"  # Soruları Markdown başlık etiketleri ile büyüt
        cevap = st.radio(formatted_soru, secenekler)
        if cevap != "Seçilmedi":  # Kullanıcı bir seçenek seçtiyse
            cevaplar[soru] = cevap
            
 
    st.markdown("<p style='font-family: Arial; font-size: 25px;'>Aşağıdaki ifadelere ne kadar katılıyorsunuz? </p>", unsafe_allow_html=True)
    
    sorular2 = [
        
        "Soru9 : İşimi tatmin edici buluyorum.",
        "Soru10 : Yaptığım işin amacını görüyorum.",
        "Soru11 : İşimin sağladığı zorluk seviyesini seviyorum.",
        "Soru12 : İşimin stres seviyesinin yönetilebilir olduğunu hissediyorum.",
        "Soru13 : Meslektaşlarım geri bildirimlerimi ciddiye alıyor.",
        "Soru14 : İş hedeflerim gerçekçi ve ulaşılabilir.",
        "Soru15 : Yöneticimin bana sağladığı mesleki gelişimden memnunum.",
        "Soru16 : Buradaki kariyer yolum konusunda netim.",
        "Soru17 : Sağlanan genel avantajlardan memnunum.",
        "Soru18 : Takım arkadaşlarım ve yöneticilerimle yeni fikirleri paylaşmaya teşvik ediliyorum.",
        "Soru19 : Bu organizasyondaki şeffaflık seviyesinden memnunum.",
    ]
    
    cevaplar2 = {}
    
    for soru in sorular2:
        secenekler = ["Seçilmedi", "Katılıyorum", "Katılmıyorum"]
        formatted_soru = f"{soru}"  # Soruları Markdown başlık etiketleri ile büyüt
        cevap = st.radio(formatted_soru, secenekler)
        if cevap != "Seçilmedi":  # Kullanıcı bir seçenek seçtiyse
            cevaplar2[soru] = cevap
    
    
    
    
    # Soru 1: Şirketimizi tavsiye etme olasılığı
    st.markdown("<p style='font-family: Arial; font-size: 20px;'>Şimdiye kadar şirketimizle olan deneyiminiz göz önüne alındığında, şirketi, saygı duyduğunuz birine tavsiye etme olasılığınız nedir?</p>", unsafe_allow_html=True)
    tavsiye_etme_olasiligi = st.slider("Lütfen 0(Çok Olası Değil) ile 10(Çok Olası) arasında bir değer seçiniz:", 0, 10)
    
    # Soru 2: Değişmek istediğiniz 3 şey
    st.markdown("<p style='font-family: Arial; font-size: 20px;'>Kuruluşumuzda değiştiğinden emin olmak istediğiniz 3 şey nedir?</p>", unsafe_allow_html=True)
    degismek_istediginiz = st.text_area("Lütfen değişmek istediğiniz 3 şeyi belirtiniz:")
    
    # Soru 3: Devam etmek istediğiniz ve sevdiğiniz 3 şey
    st.markdown("<p style='font-family: Arial; font-size: 20px;'>Kuruluşumuzda yapmaya devam ettiğimizden emin olmak istediğiniz ve en çok sevdiğiniz 3 şey nedir?</p>", unsafe_allow_html=True)
    devam_istediginiz = st.text_area("Lütfen devam etmek istediğiniz ve en çok sevdiğiniz 3 şeyi belirtiniz:")
    
    if st.button("Formu Gönder"):
        df = pd.DataFrame.from_dict(cevaplar, orient='index', columns=['Cevap'])
        df2 = pd.DataFrame.from_dict(cevaplar2, orient='index', columns=['Cevap'])
        
        # Yeni soruları veri çerçevesine eklemek
        yeni_sorular = {
            "Şirketimizi Tavsiye Etme Olasılığı": [tavsiye_etme_olasiligi],
            "Değişmek İstediğiniz 3 Şey": [degismek_istediginiz],
            "Devam Etmek İstediğiniz ve Sevdiğiniz 3 Şey": [devam_istediginiz]
        }
        df3 = pd.DataFrame.from_dict(yeni_sorular)
        
        st.write("Anketiniz başarıyla gönderildi!")
        st.write("Teşekkürler !")
        
        # MongoDB'ye veri ekleme
        client = MongoClient("mongodb+srv://onutoguzhan:9xEAlsbaGX6eDn3P@cluster0.2npecav.mongodb.net/")  # MongoDB bağlantısı
        db = client["sample_mflix"]  # Veritabanı seçimi
        collection = db["anket_cevaplari"]  # Koleksiyon seçimi
        
        # Verilerin MongoDB'ye eklenmesi
        df_dict = df.to_dict(orient="index")
        collection.insert_many(df_dict.values())
        
        df2_dict = df2.to_dict(orient="index")
        collection.insert_many(df2_dict.values())
        
        df3_dict = df3.to_dict(orient="index")
        collection.insert_many(df3_dict.values())
        
        
    
if __name__ == "__main__":
    main()
