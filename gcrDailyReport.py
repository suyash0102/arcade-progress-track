import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go

# Variable Names
date = "23-07"

# Program Variables
header = st.container()
login = st.container()
body = st.container()
owners = st.container()

# Reading the file
data = pd.read_csv("data/data.csv")
df = pd.DataFrame(data)

for i in range(len(df["Email ID"])):
    df['Email ID'][i] = df['Email ID'][i].lower()


#WebApp -- "Milestone Leaderboard"
sidebarContent = st.sidebar.radio("Menu", [
                                  "Progress Report", "Generate Badge", "Program Resources"])
# Progress Report Page
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
.last {
    font-size: 15px !important;
}

</style>
""", unsafe_allow_html=True)


def milestoneCal(quest, skillbg, game, tindex):
    rquest = int(df[" Trivia Quest Count"][tindex])
    rskillbg = int(df["Skill Badge Count"][tindex])
    rgame = int(df["Game Count"][tindex])

    if (int(df[" Trivia Quest Count"][tindex]) >= quest):
        rquest = quest
    if (int(df["Skill Badge Count"][tindex]) >= skillbg):
        rskillbg = skillbg
    if (int(df["Game Count"][tindex]) >= game):
        rgame = game
    per = int(((rquest + rskillbg+rgame) / (quest+skillbg+game)) * 100)
    return rquest, rskillbg, rgame, per


def findMilestoneLevel(tindex):
    level = 0
    cquest = int(df[" Trivia Quest Count"][tindex])
    cskillbg = int(df["Skill Badge Count"][tindex])
    cgame = int(df["Game Count"][tindex])

    if (cquest == 1 and cskillbg >= 9 and cgame>=2):
        level = 1
    if (cquest == 1 and cskillbg >= 15 and cgame>=2):
        level = 2
    if (cquest == 2 and cskillbg >= 21 and cgame>=4):
        level = 3
    if (cquest == 2 and cskillbg >= 30 and cgame>=4):
        level = 4

    return level


def showStats():
    inactive = 0
    m0Count = 0
    m1Count = 0
    m2Count = 0
    m3Count = 0
    m4Count = 0
    totalQuests = 0
    totalSkillBadges = 0

    for i in range(len(df)):
        qCount = int(df[" Trivia Quest Count"][i])
        sCount = int(df["Skill Badge Count"][i])
        gCount = int(df["Game Count"][i])

        level = 0

        if (qCount == 0 and sCount == 0 and gCount==0):
            inactive += 1

        if (qCount < 1 or sCount < 9 or gCount<2):
            if qCount == 0:
                if sCount >= 1:
                    m0Count += 1

            if sCount == 0:
                if qCount >= 1:
                    m0Count += 1

            if (qCount > 0 and sCount > 0):
                m0Count += 1

        if (qCount >= 1 and sCount >= 9 and gCount>=2):
            level = 1
        if (qCount >= 1 and sCount >= 15 and gCount>=2):
            level = 2
        if (qCount >= 2 and sCount >= 21 and gCount>=4):
            level = 3
        if (qCount >= 2 and sCount >= 30 and gCount>=4):
            level = 4

        if level == 1:
            m1Count += 1
        elif level == 2:
            m2Count += 1
        elif level == 3:
            m3Count += 1
        elif level == 4:
            m4Count += 1

        totalQuests += qCount
        totalSkillBadges += sCount

    return m0Count, m1Count, m2Count, m3Count, m4Count, totalQuests, totalSkillBadges, inactive


def prizeWinners(limit):
    finalList = []
    for i in range(len(df)):
        if(df["level"][i] == limit):
            arr = str(df["Full Name"][i]).split()
            fname = arr[0]
            lname = arr[-1]
            name = fname + " " + lname[0] + "."
            finalList.append(name)
    finalList.sort()
    return finalList


if (sidebarContent == "Progress Report"):
    with(header):
        st.image('images/banner.jpg', use_column_width=True)
        st.markdown(
            "<h1 style='text-align: center'><b>Daily Progress Report 🌩 <br> BITW</b></h1>", unsafe_allow_html=True)
        st.write("Last Updated On: " + date + "-2023")
        st.write("#####")

    with(login):
        textInput = st.text_input("Enter your Email ID").lower()

        # Input Activity
        status = False
        for i in df["Email ID"]:
            if(i == textInput):
                status = True
        if(textInput != "" and status):
            # Finding the index of the search emailID
            tindex = df[df["Email ID"] == textInput].index[0]
            st.title("Welcome " + str(df["Full Name"][tindex]) + " !")

            st.write("**Application Status:** " +
                     str(df["Application Status"][tindex]))
            st.write("**EmailID:** " + str(df["Email ID"][tindex]))
            st.write("[View Google Cloud Skills Boost Profile URL](" +
                     str(df["Public Profile URL"][tindex]) + ")")
            # st.write("**Institution:** " + str(df["Institution"][tindex]))

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<b class="big-font">Milestone Status</b>',
                        unsafe_allow_html=True)

            quest, skillbg,game, per = milestoneCal(1,9, 2, tindex)
            st.subheader("You have completed " + str(quest) +
                         " Trivia Badge and " + str(skillbg) + " Skill Badges" + str(game) + " Game Badge.")
            if(quest >= 1 and skillbg >= 9 and game>=2):
                st.balloons()

            # Milestone1
            quest, skillbg, game, per = milestoneCal(1,9, 2, tindex)
            #per = int(((quest+skillbg)/12)*100)
            st.subheader("Milestone 1:    " + str(per) + "% Completed\n Trivia Badge: " +
                         str(quest) + "/1, Skill Badge: " + str(skillbg) + "/9, Game Badge" + str(game) + "/2")
            if(quest >= 1 and skillbg >= 9 and game>=2):
                st.write(
                    "🥳 Congratulations! You have completed your 1st Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Milestone2
            quest, skillbg,game, per = milestoneCal(1,15, 2, tindex)
            st.subheader("Milestone 2:    " + str(per) + "% Completed\n Quests: " +
                         str(quest) + "/1, Skill Badge: " + str(skillbg) + "/15, Game Badge"+ str(game) + "/2")
            if (quest >= 20 and skillbg >= 10 and game>=2):
                st.write(
                    "🥳 Congratulations! You have completed your 2nd Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Milestone3
            quest, skillbg,game, per = milestoneCal(2, 21,4, tindex)
            st.subheader("Milestone 3:    " + str(per) + "% Completed\n Quests: " +
                         str(quest) + "/2, Skill Badge: " + str(skillbg) + "/21, Game Badge"+ str(game) + "/4")
            if (quest == 30 and skillbg == 15 and game>=4):
                st.write(
                    "🥳 Congratulations! You have completed your 3rd Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Ultimate Milestone
            quest, skillbg,game, per = milestoneCal(2, 30,4, tindex)
            st.subheader("Ultimate Milestone :    " + str(per) + "% Completed\n Quests: " +
                         str(quest) + "/2, Skill Badge: " + str(skillbg) + "/30, Game Badge"+ str(game) + "/4")
            if (quest >= 40 and skillbg >= 20 and game>=4):
                st.write(
                    "🥳 Congratulations! You have completed you Ultimate Milestone 🎊🎊🎊")
            else:
                st.progress(per)

        elif (textInput != "" and status == False):
            st.error("No Entry Found")

    with(owners):
        st.write("####")

# Milestone Leaderboard Page
# elif (sidebarContent == "Milestone Leaderboard"):
    with(header):
        st.image('images/banner.jpg', use_column_width=True)
        st.markdown(
            "<h1><b>Milestone Leaderboard 🏃‍♂️<br> BITW</b></h1>", unsafe_allow_html=True)
        st.write("Last Updated On: " + date + "-2023")
        st.write("#####")

    with(login):
        textInput = st.text_input("Enter your Email ID", key="email_input").lower()
        st.write("####")

    status = False

    if textInput == "admins@gcr.com":
        ml0, ml1, ml2, ml3, ml4, questTotal, skillbgTotal, inactiveCount = showStats()

        labels = ['Milestone0', 'Milestone1', 'Milestone2',
                  'Milestone3', 'Milestone4', 'Inactive']
        values = [ml0, ml1, ml2, ml3, ml4, inactiveCount]
        colors = ['cyan', 'blue', 'green', 'orange', 'gold', 'red']

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value',
                          marker=dict(colors=colors, line=dict(color='#000000', width=1)))
        st.write("## **📊 Facilitator Stats**")
        st.write("####")
        st.write("**No. of Quest completions:** " + str(questTotal))
        st.write("**No. of Skill Badge completions:** " + str(skillbgTotal))
        st.write("**Total Count:** " + str(questTotal + skillbgTotal))
        st.write("**Milestone 1 Achievers:** " + str(ml1))
        st.write("**Milestone 2 Achievers:** " + str(ml2))
        st.write("**Milestone 3 Achievers:** " + str(ml3))
        st.write("**Milestone 4 Achievers:** " + str(ml4))
        st.write("**Total Achievers:** " + str(ml1 + ml2 + ml3 + ml4))
        st.write("**Milestone 1 In Progress:** " + str(ml0))
        st.write("**Inactive Students:** " + str(inactiveCount))
        st.plotly_chart(fig)

    for i in df["Email ID"]:
        if(i == textInput):
            status = True
    if(textInput != "" and status):
        m4 = st.container()
        m3 = st.container()
        m2 = st.container()
        m1 = st.container()
        cred = st.container()

        df["level"] = 0
        for i in range(len(df)):
            quests = df[" Trivia Quest Count"][i]
            badges = df["Skill Badge Count"][i]
            game = df["Game Count"][i]
            level = 0
            if (quests >= 1 and badges >= 9 and game>=2):
                level = 1
            if (quests >= 1 and badges >= 15 and game>=2):
                level = 2
            if (quests >= 2 and badges >= 21 and game>=4):
                level = 3
            if (quests >= 2 and badges >= 30 and game>=4):
                level = 4
            df["level"][i] = level

        with(m4):
            flist = prizeWinners(4)
            # st.subheader(m1_names)
            if (len(flist) != 0):
                st.markdown(
                    '<b class="big-font">🏆 Ultimate Milestone : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                for i in flist:
                    st.write("🔸  " + str(i))
                st.markdown("<hr>", unsafe_allow_html=True)

        with(m3):
            flist = prizeWinners(3)
            # st.subheader(m1_names)
            if (len(flist) != 0):
                st.markdown(
                    '<b class="big-font">🏆 Milestone 3 : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                #st.markdown("<h2> --------* Milestone 3 : Winners *-------- </h2>", unsafe_allow_html=True)
                for i in flist:
                    st.write("🔸  " + str(i))
                st.markdown("<hr>", unsafe_allow_html=True)

        with(m2):
            flist = prizeWinners(2)
            if (len(flist) != 0):
                st.markdown(
                    '<b class="big-font">🏆 Milestone 2 : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                #st.markdown("<h2> --------* Milestone 2 : Winners *-------- </h2>", unsafe_allow_html=True)
                for i in flist:
                    st.write("🔸  " + str(i))

                st.markdown("<hr>", unsafe_allow_html=True)

        with(m1):
            flist = prizeWinners(1)
            # st.subheader(m1_names)
            if (len(flist) != 0):
                st.markdown(
                    '<b class="big-font">🏆 Milestone 1 : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                #st.markdown("<h2> --------* Milestone 1 : Winners *-------- </h2>", unsafe_allow_html=True)

                for i in flist:
                    st.write("🔸  " + str(i))

                st.markdown("<hr>", unsafe_allow_html=True)
                st.write("#####")

        with(cred):
            st.write("######")

    elif (textInput != "" and status == False):
        st.error("Sorry, we won't be able to show you the Milestone Achievers unless and until you are a Participant under Google Cloud Arcade Program Under Facilator code AF23-3E5-GAR")

elif (sidebarContent == "Generate Badge"):
    with(header):
        st.image('images/banner.jpg', use_column_width=True)
        st.markdown(
            "<h2 style='text-align: center'><b>🔖 Generate Google Cloud Arcade Badge</b></h2>", unsafe_allow_html=True)
        st.write("#####")

    with(login):
        textInput = st.text_input("Enter your Email ID").lower()

        # Input Activity
        status = False
        for i in df["Email ID"]:
            if(i == textInput):
                status = True
        if(textInput != "" and status):
            tindex = df[df["Email ID"] == textInput].index[0]
            level = findMilestoneLevel(tindex)

            if level == 0:
                st.warning("Achieve Your First Milestone  to Get your Badge")
                st.image('images/milestone0.png', use_column_width=True)
            else:
                st.success(f"You're Currently on Milestone {level}")
                image_file = st.file_uploader(
                    "Upload Image", type=['jpg', 'png', 'jpeg'])
                if image_file is not None:
                    size = (750, 750)
                    if level == 1:
                        img = Image.open(
                            "images/milestone1.png").convert("RGBA")
                    elif level == 2:
                        img = Image.open(
                            "images/milestone2.png").convert("RGBA")
                    elif level == 3:
                        img = Image.open(
                            "images/milestone3.png").convert("RGBA")
                    elif level == 4:
                        img = Image.open(
                            "images/milestone4.png").convert("RGBA")
                    elif level == 0:
                        img = Image.open(
                            "images/milestone0.png").convert("RGBA")
                    img = img.resize(size, Image.ANTIALIAS)
                    card = Image.open(image_file)

                    card = card.resize(size, Image.ANTIALIAS)

                    card.paste(img, (0, 0), img)
                    card.save("first.jpg", format="png")
                    st.image(card)
        elif (textInput != "" and status == False):
            st.error("No Entry Found")

        st.write(
            "### **Instructions on Uploading your Image and Downloading the Badge:**")
        st.write(f"""
        * You should have completed at least 1st Milestone to get your badge
        * Click on Browse Files below to Upload an image
        * Upload a Square Image to get the best version of your Badge
        * If you upload a landscape or out of shape image, it would be resized to 1:1
        * According to your Milestone, your picture will be automatically applied with a badge
        * Right click on the Image and select save image as to Download the file
        * Then do share on your social media handles by tagging us as your Facilitator [Suyash Dahake](https://www.linkedin.com/in/suyash-dahake/) [Tushar Hiwarkar](https://www.linkedin.com/in/tushar-hiwarkar-b1980b229/) and Google Cloud India, also use `#GoogleCloudReady` `#GDSCBITW` tag. Google Cloud team closely monitor this tag :smile: :tada:
        """)

else:
    with(header):
        st.image('images/banner.jpg', use_column_width=True)
        st.markdown(
            "<h2><b>Google Cloud Arcade Facilitator Program Resources</b></h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("**Program Deadline: Coming soon**")

        st.subheader("**Important Links**")
        st.write("🌐 [GOOGLE CLOUD ARCADE Facilitator '23 Program Site](https://rsvp.withgoogle.com/events/arcade-facilitator/points-system)")

        st.subheader("**Prizes**")
        st.image('images/prizes.jpeg', use_column_width=True)