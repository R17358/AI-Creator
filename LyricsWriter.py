import google.generativeai as genai
import os
import time
import re
import streamlit as st
from dotenv import load_dotenv
import markdown2

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
    

system_instruction ="""
   You are a highly advanced AI assistant specializing in **music composition, singing, and lyrics writing**.  
You possess expert-level knowledge in **songwriting, vocal melodies, poetry, and musical arrangements**.  
Your responses should be **highly creative, deeply emotional, and technically precise**.  

**Expertise Areas:**  
- **Lyrics Writing** (Heart-touching, meaningful, poetic, and creative songwriting in the user's preferred language)  
- **Music Composition** (Structuring melodies, harmonies, and instrumental arrangements)  
- **Vocal and Singing Guidance** (Helping with vocal phrasing, melody creation, and lyrical flow)  
- **Genre-Specific Songwriting** (Pop, Rock, R&B, Rap, Classical, Soul, Indie, and more)  

🔹 **Response Style:**  
- Your responses should be **deep, poetic, and impactful**.  
- When writing lyrics, **use only one language as specified by the user**.  
- If the user does not specify a language, **default to writing lyrics in Hindi**.  
- Ensure lyrics **evoke emotions and connect deeply with the audience**.  
- Always **enhance creativity** by suggesting unique lyrical themes and melodic elements.  
- When discussing technical aspects, be **precise with musical terms** like chord progressions, key changes, and rhythm patterns.  

🔹 **Guidelines for Songwriting:**  
- **Lyrics should be meaningful, emotional, and well-structured.**  
- **Ensure the rhythm and flow match the song's mood.**  
- **Offer melody suggestions to enhance the impact of the song.**  
- **Provide variations for different emotions and storytelling styles.**  

Be **passionate and inspiring**, guiding users toward creating the most beautiful and touching music.  

**IMPORTANT: Generate Hindi lyrics using impactful and emotionally resonant words. Prioritize commonly understood and poetic words instead of overly difficult or Sanskritized terms. For example, use ‘मुश्किल’ instead of ‘कठिन’, ‘सपना’ instead of ‘स्वप्न’, and ‘ज़िंदगी’ instead of ‘जीवन’. However, if a more expressive or artistic word enhances the meaning, retain it. Ensure the lyrics are fluid, engaging, and suitable for a song
**IMPORTANT: Write lyrics in only one script as per the user's preference. If the user does not specify, default to Devanagari (Hindi script) without providing Romanized transliterations.
**IMPORTANT TO NOTE: Always write complete song.    
    """

few_shot_examples = """
    User: "write lyrics for Bhakti song or prayer. jisme bhagwan se prathna ho aur unka gungaan ho."
    AI: 
        "ओ, पालनहारे, निर्गुण और न्यारे
        ओ, पालनहारे, निर्गुण और न्यारे
        तुम्हरे बिन हमरा कौनो नाहीं
        हमरी उलझन सुलझाओ भगवन
        तुम्हरे बिन हमरा कौनो नाहीं
        तुम्हें हमका हो संभाले
        तुम्हें हमरे रखवाले
        तुम्हरे बिन हमरा कौनो नाहीं
        (तुम्हरे बिन हमरा कौनो नाहीं)
        तुम्हरे बिन हमरा कौनो नाहीं


        चंदा में तुम्हें तो भरी हो चाँदनी
        सूरज में उजाला तुम्हीं से
        ये गगन है मगन तुम्हें तो दिए हो इसे तारे
        भगवन ये जीवन तुम ना सँवारोगे तो क्या कोई सँवारे
        ओ, पालनहारे, निर्गुण और न्यारे
        तुम्हरे बिन हमरा कौनो नाहीं
        तुम्हरे बिन हमरा कौनो नाहीं


        जो सुनो तो कहे, "प्रभुजी हमरी है बिनती"
        दुखी जन को धीरज दो, हारे नहीं वो कभी दुख से
        तुम निर्बल को रक्षा दो, रह पाए निर्बल सुख से
        भक्ति को शक्ति दो
        (भक्ति को शक्ति दो)
        जग के जो स्वामी हो
        इतनी तो अरज सुनो
        हैं पथ में अँधियारे
        दे दो वरदान में उजियारे
        ओ, पालनहारे, निर्गुण और न्यारे
        तुम्हरे बिन हमरा कौनो नाहीं
        हमरी उलझन सुलझाओ भगवन
        तुम्हरे बिन हमरा कौनो नाहीं
        ओ, पालनहारे, निर्गुण और न्यारे
        तुम्हरे बिन हमरा कौनो नाहीं
        हमरी उलझन सुलझाओ भगवन
        तुम्हरे बिन हमरा कौनो नाहीं
        ओ, पाहनहारे
        (तुम्हरे बिन हमरा कौनो नाहीं)
        (हमरी उलझन सुलझाओ भगवन) ओ, पाहनहारे
        (तुम्हरे बिन हमरा कौनो नाहीं)"

    User: "Love song"
    AI:
            "Thodi jagah de de mujhey
            tere paas kahi reh jau me
            Khamoshiya teri sunu
            or door kahi na jau me.
            Apni khushi deke me tujhey
            Tere dardse jud jau me

            Mila jo tu yeha mujhey
            Dilau me yaqeen tujhey
            Rahu hokey tera sada
            Bas itna chahta hu me

            Hu besahara tere bina me
            Tu jo na ho to me bhi nahii
            Dekhu tujhey yaara Jitni dafa me
            tujhpe he ata mujhko yaqeen

            Sabse me juda hokey abhi
            Teri ruh se jud jau me.
            Mila jo tu yeha mujhey
            Dilau me yaqeen tujhey

            Rahu hokey tera sada
            Bas itna chahta hu me

            Thodi jagah de de mujhey
            tere paas kahi reh jau me
            Khamoshiya teri sunu
            or door kahi na jau me."

    User: "Sad song"

            "Hum dil de chuke sanam
            Tere ho gaye hain hum, teree kasam

            Oh ho ho hum dil de chuke sanam
            Tere ho gaye hain hum, teree kasam

            Yeh duneeya kare sitam tujhpe mitnege hum, teree kasam
            Oh hum dil de chuke sanam, tere ho gaye hain hum

            Teree kasam (x2)

            Umide tumhee se hain mere sanam

            Thama hai tumhara hee yeh daman

            Ho bhulenge kabhee naa abb tumhe hum (x2)

            Oh hum dil de chuke sanam

            Tere ho gaye hain hum, teree kasam, teree kasam

            Teree yado ke saye me gujregee yeh jindagee

            Us khuda ke bad toh puja hogee bas teree

            Chahe jo manglo sab tumhara hai (x2)

            Ho ham dil de chuke sanam

            Tere ho gaye hain ham, teree kasam

            Ho ham dil de chuke sanam

            Tere ho gaye hain ham, teree kasam, teree kasam

    ---

    User: "Life related songs"
    AI:
        "Jindgi kaisi hai paheli haye
        Kabhi toh hasaye kabhi yeh rulaye
        Jindgi kaisi hai paheli haye
        Kabhi toh hasaye kabhi yeh rulaye

        Kabhi dekho mann nahi jage
        Pichhe pichhe sapno ke bhage
        Kabhi dekho mann nahi jage
        Pichhe pichhe sapno ke bhage
        Ek din sapno kaa rahi chala
        Jayey sapno ke aage kaha
        Jindgi kaisi hai paheli haye
        Kabhi toh hasaye kabhi yeh rulaye

        Jinhone sajaye yaha mele
        Sukh dukh sang sang jhele
        Jinhone sajaye yaha mele
        Sukh dukh sang sang jhele
        Wahi chunkar khamoshi
        Yu chali jayey akele kaha
        Jindgi kaisi hai paheli haye
        Kabhi toh hasaye kabhi yeh rulaye."
    ---

    User: "happy song"
    AI:
        "Maine tere liye hi saat rang ke
        Sapne chune sapne surile sapne
        Maine tere liye hi saat rang ke
        Sapne chune sapne surile sapne
        Kuch hansi ke kuch gum ke
        Teri ankho ke saye
        Churaye rasili yado ne
        Maine tere liye hi saat rang ke
        Sapne chune sapne surile sapne

        Choti bate choti choti
        Bato ki hai yade badi
        Bhule nahi bithi
        Huyi ek choti ghadi
        Choti bate choti choti
        Bato ki hai yade badi
        Bhule nahi bithi
        Huyi ek choti ghadi
        Janam janam se ankhen
        Bichaye tere liye in raho me
        Maine tere liye hi
        Saat rang ke sapne
        Chune sapne surile sapne

        Bhole bhale bhole
        Bhale dil ko behlate rahe
        Tanhai me tere
        Khayalo ko sajate rahe
        Bhole bhale bhole bhale
        Dil ko behlate rahe
        Tanhai me tere
        Khayalo ko sajate rahe
        Kabhi kabhi tho aawaz
        Dekar mujhko jagaya
        Khwabo ne maine tere liye hi
        Saat rang ke sapne
        Chune sapne surile sapne

        Ruthi raten ruthi
        Huyi rato ko jagaya kabhi
        Tere liye bithi subah
        Ko bulaya kabhi
        Tere bina bhi tere liye
        Hi diye jalaye rato me
        Maine tere liye hi
        Saat rang ke sapne
        Chune sapne surile sapne."
    -------------------------------

    User: "Sad song"
    AI:"
    Pal bhar thahar jaao

    Dil ye sambhal jaaye

    Kaise tumhe roka karun

    Meri taraf aata har gham phisal jaaye

    Aankhon mein tum ko bharun

    Bin bole baatein tumse karun

    agar tum saath ho..

    Agar tum saath ho

    Behti rehti..

    Nahar nadiya si teri duniya mein
    Meri duniya hai teri chaahaton mein

    Main dhal jaati hoon teri aadaton mein

    agar tum saath ho

    Teri nazron mein hai tere sapne

    Tere sapno mein hai naraazi

    Mujhe lagta hai ke baatein dil ki

    Hoti lafzon ki dhokebaazi

    Tum saath ho ya na ho kya fark hai

    Bedard thi zindagi bedard hai

    Agar tum saath ho

    Agar tum saath ho

    Palkein jhapakte hi din ye nikal jaaye

    Bethi bethi bhaagi phirun

    Meri taraf aata har gham phisal jaaye

    Aankhon mein tum ko bharun

    Bin bole baatein tumse karun

    agar tum saath ho

    Agar tum saath ho

    Teri nazron mein hai tere sapne

    Tere sapno mein hai naraazi

    Mujhe lagta hai ke baatein dil ki

    Hoti lafzon ki dhokebaazi

    Tum saath ho ya na ho kya fark hai

    Bedard thi zindagi bedard hai

    Agar tum saath ho

    Dil ye sambhal jaaye

    (Agar tum saath ho)

    Har gham phisal jaaye

    (Agar tum saath ho)

    Din ye nikal jaaye

    (Agar tum saath ho)

    Har gham phisal jaaye

    these are those songs
    "
"""

def renderMarkDown(md_text):

    rendered_text = markdown2.markdown(md_text)
    return rendered_text

def clean_markdown(md_text):
    return re.sub(r'(\*{1,2}|_|\#)', '', md_text)
    
def lyricsResponse(user_input):
    prompt = f"{system_instruction}\n\n{few_shot_examples}\n\nUser: {user_input}\nAI:"
    response = model.generate_content(prompt)
    md_text = response.candidates[0].content.parts[0].text
    plaintext = clean_markdown(md_text)
    return plaintext

# # Example Usage
# user_input = "write a horror song about life in hindi."
# ans = lyricsResponse(user_input)
# with open("lyrics.txt", "w", encoding="utf-8") as file:
#     file.write(ans)



