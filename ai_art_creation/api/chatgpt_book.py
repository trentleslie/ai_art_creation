import openai
import random
from ai_art_creation.api.api_key import api_key, chatgpt_model
import time
import os
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# The ID of a sample document.
FOLDER_ID = "1BcFn1rubER0q0FPepEeDEwh-cy_OUFoX"

def google_connect():
    global docs_service
    global drive_service
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\api\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
    except HttpError as err:
        print(err)

google_connect()

def create_new_google_doc(doc_name, doc_text, folder_id):
    global docs_service
    global drive_service
    service = docs_service

    # Create a new document
    document = {
        'title': doc_name
    }
    doc = service.documents().create(body=document).execute()
    document_id = doc['documentId']

    # Add the specified text to the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': doc_text
            }
        }
    ]
    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    # Move the document to the specified folder
    file = drive_service.files().get(fileId=document_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    file = drive_service.files().update(fileId=document_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents').execute()

    return document_id


'''
def create_new_google_doc(doc_name, doc_text, folder_id):
    # Create a new document in the specified folder
    doc = docs_service.documents().create(body={'title': doc_name, 'parents': [folder_id]}).execute()

    # Find the end index of the document
    end_index = doc['body']['content'][-1]['endIndex']

    # Create requests for adding text at the end
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index - 1
                },
                'text': doc_text
            }
        }
    ]

    # Execute the requests
    result = docs_service.documents().batchUpdate(documentId=doc['documentId'], body={'requests': requests}).execute()
    return result
'''

def append_to_google_doc(doc_id, text):
    # Get the document
    doc = docs_service.documents().get(documentId=doc_id).execute()

    # Find the end index of the document
    end_index = doc['body']['content'][-1]['endIndex']

    # Create requests for adding text at the end
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index - 1
                },
                'text': text
            }
        }
    ]

    # Execute the requests
    result = docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return result

pre_context = "This is the first chapter of the book, so there is no prior context."

book_outline_str = '''  Chapter 1: The Enchanted City
                        1.1. The Beauty of Ak'tuun B'aakal: The chapter opens with a vivid description of the mythical city of Ak'tuun B'aakal, showcasing its unique architecture, landscape, and harmonious lifestyle.
                        1.2. Introducing the Trio: Yaxchel, Ix'Kanul, and B'alam are introduced through their daily activities, highlighting their roles and responsibilities within the city.
                        1.3. A Peaceful Existence: The peaceful and harmonious lifestyle in Ak'tuun B'aakal is described, showing the love and support among the community members.
                        1.4. Subtle Omens: Foreshadowing of the impending disaster through subtle hints, such as unusual occurrences or a feeling of unease among the characters.
                        1.5. Bonds of Friendship: Yaxchel and Ix'Kanul's close friendship is established, revealing their trust and loyalty towards each other.

                        Chapter 2: Hidden Desires
                        2.1. Personal Lives Unveiled: The personal lives of Yaxchel, Ix'Kanul, and B'alam are explored, including their families and relationships.
                        2.2. Introducing Secondary Characters: The spouses of Yaxchel and Ix'Kanul, and other close friends are introduced, providing a more extensive understanding of the characters' social circle.
                        2.3. Strengths, Weaknesses, and Wishes: Each character's strengths, weaknesses, and desires are explored, providing depth to their personalities.
                        2.4. The Tradition of Arranged Marriages: The arranged marriage system in Ak'tuun B'aakal is introduced, and its impact on the community is discussed.
                        2.5. Forbidden Love: Yaxchel and Ix'Kanul's secret love is revealed, setting the stage for their emotional journey.
                    '''
                    
book_outline_str2 = '''Chapter 3: The Mysterious Plague
                        3.1. The Onset of Disease: The mysterious disease first appears and rapidly spreads through the city, causing panic and distress among the citizens.
                        3.2. Symptoms and Suffering: The symptoms and impact of the disease on the infected are described, evoking empathy from the reader.
                        3.3. Emotional Turmoil: Characters lose loved ones to the disease, capturing the emotional resonance of their grief.
                        3.4. The Desperate Search for a Cure: The urgency for finding a cure is established, pushing the characters to take action.
                        3.5. Coping Mechanisms: The community's initial reactions and coping mechanisms are shown, including the responses of secondary characters.

                        Chapter 4: Traditional Healing
                        4.1. Yaxchel and Ix'Kanul's Attempts: Yaxchel and Ix'Kanul try to find a cure using traditional methods and their knowledge of healing practices.
                        4.2. The Spread Continues: The disease continues to spread, increasing tension and stakes for the characters and the community.
                        4.3. A Community's Resilience: The theme of survival and community strength is explored, highlighting the perseverance of the citizens.
                        4.4. Despair and Hopelessness: The characters grapple with feelings of despair and hopelessness as the disease's toll mounts.
                        4.5. A Glimmer of Hope: Yaxchel learns about a sacred plant that may have healing properties, sparking new hope in their quest for a cure.

                        Chapter 5: The Dangerous Quest
                        5.1. Sharing the Knowledge: Yaxchel shares the information about the sacred plant with Ix'Kanul and B'alam, and they decide to embark on a dangerous quest to find it.
                        5.2. B'alam's Wisdom: B'alam shares valuable guidance and insights about the plant, its location, and the challenges they may face on their journey.
                        5.3. Community Support: The community, including secondary characters, offers support and encouragement for their journey, showing unity in the face of adversity.
                        5.4. Preparations Begin: The characters prepare for their quest, developing pacing through action and tension as they gather supplies and say their goodbyes.
                        5.5. Yaxchel's Motivation: Yaxchel's husband falls ill, motivating her to press forward and find the sacred plant to save him and the community.

                        Chapter 6: Into the Unknown
                        6.1. The Jungle Awaits: The characters venture deeper into the jungle, encountering the lush, vivid environment and its hidden dangers.
                        6.2. Conflicting Emotions: Yaxchel and Ix'Kanul face internal conflicts about their love and responsibilities towards their families and community.
                        6.3. B'alam's Teachings: B'alam shares his wisdom and knowledge about the jungle, teaching the characters valuable survival skills.
                        6.4. First Major Challenge: The characters face their first major challenge in the jungle, testing their resilience, resourcefulness, and teamwork.
                        6.5. Overcoming Adversity: The characters overcome the initial challenge, growing closer together and learning from the experience.

                        Chapter 7: Deepening Bonds
                        7.1. Love Amidst Danger: The forbidden love subplot develops as Yaxchel and Ix'Kanul share intimate moments, deepening their connection despite the risks.
                        7.2. New Obstacles: The characters encounter new challenges and obstacles in the jungle, testing their limits and forcing them to rely on each other.
                        7.3. Growing Strength: Yaxchel, Ix'Kanul, and B'alam's bond grows stronger, helping them face adversity with a united front.
                        7.4. Emotional Complexity: The emotional depth and conflict created by Yaxchel and Ix'Kanul's love are explored, heightening the stakes of their journey.
                        7.5. Navigating the Perilous Path: The characters navigate the treacherous jungle, learning to adapt and survive in the hostile environment.

                        Chapter 8: Setbacks and Hope
                        8.1. Searching for the Sacred Plant: Yaxchel and Ix'Kanul face setbacks in their search for the sacred plant, struggling to find clues to its location.
                        8.2. Emotional Resonance: Fear and loss are emphasized as the disease claims more lives in Ak'tuun B'aakal, motivating the characters to push forward.
                        8.3. A Mysterious Clue: A mysterious clue about the disease's origin is revealed, raising questions about its connection to the city's past.
                        8.4. B'alam's Comfort: B'alam offers guidance and comfort to Yaxchel and Ix'Kanul, helping them maintain hope in the face of adversity.
                        8.5. Renewed Determination: The characters find renewed determination and hope, vowing to find the sacred plant and save their city.

                        Chapter 9: The Ancient Site
                        9.1. Discovering Secrets: The characters discover an ancient site connected to the disease, uncovering hidden knowledge about its origin.
                        9.2. Unraveling the Mystery: A twist reveals new information about the disease's origin, forcing the characters to grapple with the implications of this revelation.
                        9.3. A Sense of Awe: The ancient site is described in vivid detail, showcasing the unique voice and style of the author.
                        9.4. A Powerful Lesson: B'alam teaches the characters a powerful lesson about the consequences of the past, urging them to learn from history.
                        9.5. The Path Forward: The characters develop a plan to find the sacred plant and address the newly discovered information about the disease's origin.

                        Chapter 10: The Sacred Plant
                        10.1. The Final Stretch: The characters press on with renewed determination, drawing closer to the location of the sacred plant.
                        10.2. Hidden Beauty: The sacred plant's location is described, showcasing the breathtaking beauty and mystique of the environment.
                        10.3. The Moment of Truth: The characters finally locate the sacred plant, experiencing a mixture of joy, relief, and trepidation as they prepare to harvest it.
                        10.4. An Unexpected Consequence: The characters face an unforeseen consequence of obtaining the sacred plant, adding a new layer of tension to their quest.
                        10.5. A Daring Escape: The characters must work together to escape the consequences and secure the sacred plant, highlighting their growth as a team.

                        Chapter 11: The Return Journey
                        11.1. A Race Against Time: The characters race back to Ak'tuun B'aakal with the sacred plant, driven by urgency as the disease continues to claim lives.
                        11.2. The Weight of Responsibility: The emotional burden of their responsibility is explored as the characters grapple with the consequences of their actions and the lives at stake.
                        11.3. Unresolved Feelings: Yaxchel and Ix'Kanul confront their unresolved feelings for each other, adding complexity to their relationship.
                        11.4. Perseverance and Resilience: The characters continue to face challenges on their return journey, showcasing their growth and determination.
                        11.5. A Glimpse of Hope: As the characters near Ak'tuun B'aakal, they receive news of a positive development, providing a glimpse of hope and encouragement.

                        Chapter 12: The Cure and Revelation
                        12.1. A Hero's Welcome: The characters return to Ak'tuun B'aakal, receiving a hero's welcome and appreciation from the community.
                        12.2. Administering the Cure: The characters begin administering the cure derived from the sacred plant, witnessing its miraculous healing effects.
                        12.3. The Community's Recovery: The city of Ak'tuun B'aakal starts to recover, with the characters and community members working together to rebuild and heal.
                        12.4. Sharing the Truth: The characters reveal the truth about the disease's origin and the lessons learned from the ancient site, urging the community to confront their past.
                        12.5. Embracing Change: The community begins to embrace change and a new way of life, signaling a shift in their culture and values.

                        Chapter 13: Healing Hearts
                        13.1. Reconciling Relationships: Yaxchel and Ix'Kanul face the consequences of their forbidden love, striving to repair their relationships with their families.
                        13.2. Emotional Turmoil: The emotional aftermath of their journey is explored, as the characters confront their feelings and personal losses.
                        13.3. Growth and Transformation: The characters experience personal growth and transformation, learning from their experiences and emerging stronger.
                        13.4. B'alam's Wisdom: B'alam continues to share his wisdom and guidance, helping the characters navigate their emotional struggles.
                        13.5. Forgiveness and Healing: The characters and their loved ones begin the process of forgiveness and healing, finding closure and rebuilding their lives.

                        Chapter 14: A New Beginning
                        14.1. A Rebuilt City: The city of Ak'tuun B'aakal is rebuilt, reflecting the community's resilience and unity in the face of adversity.
                        14.2. The Power of Love: Yaxchel and Ix'Kanul's love story reaches a resolution, demonstrating the transformative power of love in their lives.
                        14.3. Community Growth: The community embraces change and growth, incorporating new values and practices to prevent the past's mistakes from repeating.
                        14.4. B'alam's Legacy: B'alam's wisdom and teachings leave a lasting impact on the characters and the community, securing his legacy as a guiding figure.
                        14.5. New Leadership: Yaxchel and Ix'Kanul assume new leadership roles within the community, using their experiences to drive positive change and growth.

                        Chapter 15: Reflection and Gratitude
                        15.1. Remembering the Past: The characters and the community remember those who were lost to the disease, honoring their memories and sacrifices.
                        15.2. Lessons Learned: The characters reflect on the lessons they learned from their journey, acknowledging their personal growth and transformation.
                        15.3. Gratitude for Life: The characters express gratitude for their lives, newfound wisdom, and the opportunity to make a difference in their community.
                        15.4. A Time for Celebration: The community comes together to celebrate their triumph and resilience, marking a new chapter in their lives.
                        15.5. Strengthened Bonds: The strengthened bonds between the characters and the community are showcased, reflecting the love and support that helped them overcome adversity.

                        Chapter 16: Building a Brighter Future
                        16.1. New Priorities: The characters and the community set new priorities, focusing on sustainability, equity, and the well-being of all citizens.
                        16.2. Educational Initiatives: New educational initiatives are launched, aiming to preserve the knowledge and wisdom gained from their journey and experiences.
                        16.3. Cultural Shifts: The community experiences cultural shifts, embracing new values and practices that promote harmony and prevent future catastrophes.
                        16.4. The Ripple Effect: The positive changes in Ak'tuun B'aakal inspire surrounding communities, demonstrating the potential for widespread impact.
                        16.5. A Lasting Impact: The story of Yaxchel, Ix'Kanul, and B'alam's quest leaves a lasting impact on future generations, inspiring hope and perseverance.

                        Chapter 17: An Unexpected Discovery
                        17.1. A Mysterious Artifact: A mysterious artifact is discovered, hinting at the existence of other ancient sites and hidden knowledge.
                        17.2. Excitement and Curiosity: The characters and the community express excitement and curiosity about the artifact and the potential for new discoveries.
                        17.3. Ancient Connections: The artifact suggests a connection between Ak'tuun B'aakal and other ancient civilizations, sparking interest in exploring their shared history.
                        17.4. Expanding Horizons: The community begins to expand its horizons, embarking on new quests for knowledge and understanding.
                        17.5. The Promise of Adventure: The characters prepare for new adventures, driven by their desire to uncover more about their world and their history.

                        Chapter 18: A World Beyond
                        18.1. New Discoveries: The characters embark on new adventures, discovering more about the world beyond Ak'tuun B'aakal and its ancient connections.
                        18.2. Unexpected Challenges: The characters face unexpected challenges on their new journeys, testing their resilience and resourcefulness.
                        18.3. Forming Alliances: The characters form alliances with other communities, fostering cooperation and a shared pursuit of knowledge.
                        18.4. Unraveling Mysteries: The characters uncover more about the mysterious artifact, revealing new insights into their world and its history.
                        18.5. Expanding Knowledge: The characters and the community expand their knowledge and understanding of their world, embracing a more inclusive and interconnected perspective.

                        Chapter 19: A Legacy of Wisdom
                        19.1. Sharing Knowledge: The characters share their newfound knowledge and experiences with their community, strengthening the bonds between them and fostering growth.
                        19.2. B'alam's Teachings Revisited: The characters reflect on B'alam's teachings, recognizing the lasting impact of his wisdom on their lives and community.
                        19.3. The Importance of Balance: The characters and the community learn the importance of maintaining balance between progress and preservation, ensuring a sustainable future.
                        19.4. Embracing Diversity: The community embraces diversity and inclusion, recognizing the value of different perspectives and experiences in their collective growth.
                        19.5. A Brighter Tomorrow: The characters and the community look towards a brighter future, inspired by their journey and the potential for continued growth and prosperity.

                        Chapter 20: A New Era
                        20.1. A Flourishing Community: Ak'tuun B'aakal flourishes as a result of the changes and growth inspired by the characters' journey, showcasing the power of unity and resilience.
                        20.2. A Strong Foundation: The community establishes a strong foundation for future generations, ensuring that the lessons of the past are not forgotten.
                        20.3. Yaxchel and Ix'Kanul's Legacy: Yaxchel and Ix'Kanul's love story and their dedication to their community leave a lasting impact, inspiring hope and perseverance.
                        20.4. B'alam's Enduring Influence: B'alam's wisdom continues to guide the community, serving as a reminder of the importance of humility, learning, and compassion.
                        20.5. A Story of Hope: The story of Ak'tuun B'aakal and its people serves as a beacon of hope for others, symbolizing the power of love, unity, and the human spirit in overcoming adversity.'''

def text_to_dict(text):
    chunks = [chunk.strip() for chunk in text.split('\n\n')]
    chapter_dict = {}
    chapter_title = ""
    print(chunks)

    for chunk in chunks:
        lines = [line.strip() for line in chunk.split('\n')]
        for line in lines:
            if line.startswith("Chapter"):
                chapter_title = line
                chapter_dict[chapter_title] = {}
            else:
                section_title, summary = line.strip().split(": ", 1)
                chapter_dict[chapter_title][section_title] = summary

    return chapter_dict

book_outline_dict = text_to_dict(book_outline_str)

def generate_draft_chapter(pre_context, summary, folder_id, chapter_title, section_title):
    
    time.sleep(3)
    
    # Set your OpenAI API key
    openai.api_key = api_key

    system_prompt = f'''You are a world class, best-selling author that never forgets the following fundamental elements of story-telling:
                            Fundamental elements for consideration:
                            Engaging plot: Intriguing, well-structured narrative with a clear arc.
                            Relatable characters: Memorable, well-developed personalities.
                            Emotional resonance: Evoking strong emotions and leaving lasting impressions.
                            Conflict and tension: Driving the story with internal and external challenges.
                            Pacing: Balancing action, dialogue, and description to maintain engagement.
                            Unique voice and style: Distinctive authorial voice and writing style.
                            Universal themes: Exploring relatable themes that resonate with a wide audience.
                            Strong world-building: Creating vivid, immersive, and believable settings.
                            Genre conventions: Utilizing and innovating within familiar genre elements.
                            Marketing and visibility: Effective promotion and presentation to reach readers.
                        You write with a 100% unique, creative, and in a human-like style, using contractions, idioms, transitional phrases, interjections, dangling modifiers,
                        and colloquialisms, and avoiding repetitive phrases and unnatural sentence structures. 
                        The story overview is as follows:
                        Book Introduction:
                            In the heart of the impenetrable jungles of Central America, hidden beneath centuries of overgrown foliage, lies the mythical lost city of La Ciudad Blanca, known to its inhabitants as Ak'tuun B'aakal. Steeped in legend and mystery, the city has remained untouched by the passage of time, its people living in harmony with the ancient spirits that protect their sacred land. But this sanctuary of peace and abundance is about to be confronted by a force it has never faced before - a force that threatens to annihilate the very essence of their existence.
                            Whispers of the Lost City chronicles the harrowing story of the people of Ak'tuun B'aakal as they face an invisible enemy that leaves only devastation in its wake. As the disease with flu-like symptoms and rashes that appear on the face, hands, and forearms spreads like wildfire through the populace, claiming the lives of the majority, the survivors are left reeling in the aftermath of the tragedy. Plagued by fear and desperation, the few who remain must grapple with the question of why this has happened to them and what they must do to ensure their survival.
                            Guided by a motley group of characters - a brave warrior, a gifted healer, a cunning shaman, and a wise elder - the survivors embark on a perilous journey to unravel the truth behind the enigmatic disease that has ravaged their once-thriving city. As they delve deeper into the secrets of their ancestors, they find themselves caught in a web of intrigue, deceit, and betrayal, revealing the dark underbelly of a city that had always seemed like a utopia.
                            The author masterfully weaves together history, mythology, and suspense to create a gripping tale of survival, love, and sacrifice set against the lush backdrop of the Central American rainforest. This compelling narrative, rich with historical detail and vivid descriptions, transports readers into a world where the line between reality and legend blurs, and where the whispers of the lost city echo through time, reminding us that the past is never truly lost.
                        Main Characters:
                            Yaxchel - A wise and skilled healer who plays a pivotal role in discovering the healing properties of a sacred plant. Yaxchel's knowledge and courage help the people of Ak'tuun B'aakal to combat the mysterious disease that threatens their city.
                            Ix'Kanul - A brave warrior and close friend of Yaxchel, Ix'Kanul joins the healer on a quest to find the sacred plant. His strength and determination are instrumental in overcoming the challenges they face in the jungle.
                            B'alam - A respected elder of Ak'tuun B'aakal, B'alam provides guidance and wisdom to Yaxchel and Ix'Kanul during their journey. B'alam's experience and knowledge of the city's history help them navigate the difficult path ahead.
                        Subplot:
                            A love story between Yaxchel and Ix'Kanul, set against the backdrop of a society where arranged marriages were the norm, could add an element of tension and emotional depth to the story of Ak'tuun B'aakal.
                            Their love story could be portrayed as a forbidden romance, with Yaxchel and Ix'Kanul forced to keep their feelings hidden from their respective spouses and the rest of their community. The fear of discovery and the social consequences of their actions could add to the stakes of the story and create additional conflict and tension.
                            Their relationship could be portrayed as a source of strength and inspiration for both characters, allowing them to find solace and comfort in each other's company despite the difficult circumstances they face. It could also serve as a reminder of the power of love to overcome social norms and expectations, and inspire the people of Ak'tuun B'aakal to question the status quo and forge their own paths.
                            Overall, incorporating a love story into the plot of Ak'tuun B'aakal could add a layer of emotional depth and nuance to the story, making it more engaging and relatable to readers.
                        For context only, this is the story leading up to the chapter you are about to write:
                            {pre_context}
                        You are currently writing Section {section_title} of {chapter_title}. This is the only section you are writing. Do not write the entire book. Do not write the about other sections, chapters, or parts of the story. The chapter should be no less than 1,000 words.
                        This is the summary of the chapter you are about to write:
                            {summary}
                        Only write this current section. Do not write the entire book. The chapter should be no less than 1,000 words. 
                        If there is more than one character being discussed, incorporate compelling and unique dialogue between them that would be consistent with their personalities.
                        '''
                                
    user_prompt = f'''Write Section {section_title} of {chapter_title} with the summary "{summary}" that is no less than 1,000 words. 
                        This is the only section you are writing. Do not write the entire book. 
                        If there is more than one character being discussed, incorporate compelling and unique dialogue between them that would be consistent with their personalities.'''
                                
    # Define a list of styles
    style = random.choice(['compelling blog post']
    )

    #build messages payload
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": style},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": user_prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = 0.5,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )


    # Extract the generated text from the API response
    draft_chapter = (response['choices'][0]['message']['content'])

    doc_id = create_new_google_doc(f'{chapter_title} - {section_title}', draft_chapter, folder_id)
    print(doc_id)

    return draft_chapter

for chapter_title, sections_dict in book_outline_dict.items():
    for section_title, summary in sections_dict.items():
        pre_context = generate_draft_chapter(
            pre_context = pre_context,
            summary = summary,
            folder_id = FOLDER_ID,
            chapter_title = chapter_title,
            section_title = section_title
        )
        print(f'Chapter: {chapter_title}, Section: {section_title} completed.')