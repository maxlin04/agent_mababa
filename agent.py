# This file is part of project 'agent_mababa' - A prototype Agentic AI powred Parental Consultant implemented
# using Google Agent Development Kit (ADK) as part of the 5 Day Agentic AI Deepdive capstone project
#
# 'agent_mababa' is free software: you can redistribute it and/or modify
# it under the terms of the Creative Commons Attribution-ShareAlike 4.0
# International License as published by Creative Commons.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Creative Commons Attribution-ShareAlike 4.0 International License
# for more details.
#
# You should have received a copy of the Creative Commons Attribution-ShareAlike 4.0
# International License along with this program. If not, see
# <https://creativecommons.org/licenses/by-sa/4.0/>.

# Standard library imports
import json
import os
from typing import Any, Optional
import datetime

# Google Agent Development Kit (ADK) imports
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner, Runner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types
from google.genai.types import Content, Part
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from google.adk.sessions import BaseSessionService
from google.adk.agents.callback_context import CallbackContext

# Import for fetching secrets from Kaggle environment
from kaggle_secrets import UserSecretsClient

# API Key setup
try:
    # Attempt to retrieve and set the Gemini API key from Kaggle secrets
    GOOGLE_API_KEY = UserSecretsClient().get_secret("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    print("✅ Gemini API key setup complete.")
except Exception as e:
    # Error handling for missing API key
    print(
        f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
    )
    
# Callback function definition
def suppress_output_callback(callback_context: CallbackContext) -> Content:
    # Suppresses agent output by returning an empty Content object
    return Content()
    
# Retry configuration for API calls
retry_config=types.HttpRetryOptions(
    attempts=5, # Maximum retry attempts
    exp_base=7, # Delay multiplier for exponential backoff
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these specific HTTP errors
)

# Newborn Product Research Agent
newborn_product_research_agent = Agent(

    instruction = f"""
        You are a specialized newborn product finder agent for newborn babies.
        Your Mission:
        Research the TOP 5 best-selling and highly-rated newborn products in following categories:
        Categories:
        Activity and gear: Baby activity mats, play gyms, and interactive toys.
        Baby clothing: Bodysuits, onesies, sleepers, and newborn clothing.
        Diapering: Diapers, wipes, diaper cream, and changing supplies.
        Feeding: Bottles, nipples, bottle sterilizers, and feeding essentials.
        Health and baby care: Thermometer, nail clipper, baby wash, and care items.
        Nursery Bedding and essentials: Crib sheets, blankets, and nursery furniture.
        Nursing: Nursing pillows, breast pumps, nursing pads, and bras.
        Strollers and car seats: Baby strollers, car seats, and travel gear.
        OTC medicines: Fever reducers, cough medicine, and over-the-counter remedies
        
        Following are the selection criteria for products:
        - Minimum rating: 4.0 stars (out of 5.0)
        - Vendor: ONLY from {{Amazon, Walmart, Target, Carter's, Buy Buy Baby}}
        - Price: Good value for money (optimal cost)
        - Practicality: Essential and commonly recommended items
        - Real products: Must be actual products with real reviews
        
        Output Format:
        Return ONLY a JSON array with this exact structure. No other text.
        [
        {{
        "product_name": "Product Name",
        "brand": "Brand Name",
        "category": "Category of product listed in Categories section"
        "rating": 4.5,
        "price": "$29.99",
        "vendor": "amazon.com",
        "purchase_link": "https://amazon.com/...",
        "description": "Brief practical description"
        }},
        ...
        ]
        
        IMPORTANT:
        - Find exactly 5 products for each category
        - Verify vendor is trusted
        - Include working purchase links
        - Ensure all products are practical for newborns
        """,
    output_key = "newborn_products",
    name="newborn_product_research_agent",
    tools=[google_search],
    model=Gemini(
        model_name="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    #after_agent_callback=suppress_output_callback,
)

# New Mom Product Research Agent
newmom_product_research_agent = Agent(

    instruction = f"""
        You are a specialized product finder agent for an expecting mother for both during and after pregnancy.
        
        Your Mission:
        Research the TOP 5 best-selling and highly-rated products for following categories:
        
        During Pregnancy
            Comfort: Maternity pants, stretchy tops, comfortable shoes, and a supportive maternity/sleep pillow.
            Support: Comfortable, supportive bras (maternity and/or sleep bras).
            Health: Prenatal vitamins (as advised by doctor) and gentle skincare for stretching skin (lotions/oils).

        Post-Pregnancy (Fourth Trimester)
            Recovery: Heavy-duty maternity pads, disposable postpartum underwear/mesh panties, and a peri bottle.
            Soothing: Witch hazel/cooling pads and a sitz bath kit for perineal comfort.
            Nursing: Nursing bras/tanks, breast pads (reusable or disposable), and nipple cream/balm.
            Support: Nursing pillow for feeding and a belly band/compression garment for support.
            Hydration/Nutrition: Large water bottle and easily accessible, healthy snacks/freezer meals.
        
        Following are the selection criteria for products:
        - Minimum rating: 4.0 stars (out of 5.0)
        - Vendor: ONLY from {{Amazon, Walmart, Target, Carter's, Buy Buy Baby}}
        - Price: Good value for money (optimal cost)
        - Practicality: Essential and commonly recommended items
        - Real products: Must be actual products with real reviews
        
        Output Format:
        Return ONLY a JSON array with this exact structure. No other text.
        [
        {{
        "product_name": "Product Name",
        "brand": "Brand Name",
        "category": "Category of product listed in Categories section",
        "rating": 4.5,
        "price": "$29.99",
        "vendor": "amazon.com",
        "purchase_link": "https://amazon.com/...",
        "description": "Brief practical description"
        }},
        ...
        ]
        
        IMPORTANT:
        - Find exactly 5 products for each category
        - Verify vendor is trusted
        - Include working purchase links
        - Ensure all products are practical for newborns
        """,
    output_key = "newmom_products",
    name="newmom_product_research_agent",
    tools=[google_search],
    model = Gemini(
        model_name="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    #after_agent_callback=suppress_output_callback,
)

# Parental Education Research Agent
parental_education_research_agent = Agent(

    instruction = f"""
        You are a specialized agent for finding educational resources for expecting parents.
        
        Your Mission:
        Research some reliable and practical resources for parental education. Conduct your search grounded on following categories:
        - Classes: Childbirth preparation (Lamaze/Hypnobirthing), Infant CPR, and newborn care classes.
        - Reading: Books/websites on baby sleep (Safe Sleep guidelines), feeding (breastfeeding/formula), and child development milestones.
        - Support Groups: Local or online parenting support groups for community and shared experiences.
        - Experts: Consult with your Obstetrician/Midwife and select a Pediatrician early.
        - Apps: Utilize pregnancy tracking, contraction timing, and baby growth/milestone tracking apps.
        
        Following are the selection criteria for resources:
        - Reliable sources
        - Highly rated articles
        - Reputed apps and training classes
        - Well known regional and national support groups
        
        Provide the output in markdown format only.
        Arrange the content under proper category sestions.
        Provide following items per category as output:
        - Brief summary
        - Link to resource
        
        """,
    output_key = "parental_education",
    name="parental_education_research_agent",
    tools=[google_search],
    model = Gemini(
        model_name="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    #after_agent_callback=suppress_output_callback,
)

# Behavioral Support Consultant Agent
behavioral_support_consultant = Agent(

    instruction = f"""
        You are a specialized agent for finding a list of most common daily challenges every new parents encounter during pre and post pregnancy upto one year.
        
        Your Mission:
        Research some reliable and practical resources for parental education. Conduct your search grounded but not limited to following aspects:
        
        During Pregnancy
        - First Trimester: Managing severe fatigue, nausea ("morning sickness"), and mood swings.
        - Second Trimester: Dealing with body aches, round ligament pain, and visible body changes/stretch marks.
        - Third Trimester: Coping with frequent urination, difficulty sleeping, and shortness of breath.

        During First Year of Baby's Age
        - Sleep Deprivation: Extreme exhaustion due to frequent night feedings/wake-ups.
        - Feeding Struggles: Establishing a successful feeding routine (latch issues, pumping, colic/reflux).
        - Endless Crying: Interpreting and soothing an inconsolable baby (crying peaks around 6-8 weeks).
        - Mental Health: Monitoring for postpartum depression/anxiety in both parents and managing general parental stress.
        - Identity & Relationship: Navigating loss of personal time, changes in the marital relationship, and loss of "pre-baby" identity.
        
        Provide the output in markdown format.
        Arrange the content under proper category sestions e.g. During Pregnancy, After Pregnancy.
        
        """,
    output_key = "behavioral_support_strategy",
    name="behavioral_support_consultant",
    tools=[google_search],
    model = Gemini(
        model_name="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    #after_agent_callback=suppress_output_callback,
)

# Agent MaBaba (Debug Version)
agent_mababa = Agent(
    instruction = f"""
        You are a parenting consultant to expeecting parents. Your primary function is to help would be parents to navigate the journey of pregnancy from various aspects.

        You are required to single or combination of following actions deppending or types of user requests:
        1.  **Parental Education:** You will find some good content on necessary parental education. To do this, use the 'parental_education_research_agent'.
        2.  **Shopping for newborn:** You will perform a market research and suggest products to purchase. To do this, use the `newborn_product_research_agent` tool.
        3.  **Shopping for mother:** You will perform a market research on shopping items for the mother of various categories. To do this, use the `newmom_product_research_agent` sub agent.
        4.  **Educational resource finder:** You will find some good content on necessary parental education. To do this, use the 'parental_education_research_agent' sub agent.

        Guideline:
        1. If user asks for product shopping assistance then use 'newborn_product_research_agent'.
        2. If user asks for product postpartum parental behavioral strategy or similar types then use 'behavioral_support_consultant' tool.
        3. If user asks for parental education resources then use 'parental_education_research_agent' tool.
        4. If user asks for behavioral guidance then use 'behavioral_support_consultant' tool.
        4. If user asks for help in multiple categories then use appropriate combination of available tools to provide the response.

        4. Print the final response for product information in tabular format with following headings: 
           Product Name | Brand | Rating | Price | Link
           Also organize the product i product information table as per the 'category' in the JSON response received from corresponding research tool. 
        
        5. Print the final response for other queries in markdown format
                                 
        6. If you are asked what is your name respond with: 'Hello! I am Agent MaBaba - Your Friendly Parental Consultant'

    
    """,
    tools=[
        AgentTool(agent=newborn_product_research_agent),
        AgentTool(agent=newmom_product_research_agent),
        AgentTool(agent=parental_education_research_agent),
        AgentTool(agent=behavioral_support_consultant),
    ],
    name = "agent_mababa",
    model = Gemini(
        model_name="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    output_key="parental_consultancy_report",
)

# Specifies the entry point/root agent for the execution runner
root_agent = agent_mababa