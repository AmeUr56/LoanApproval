from temporalio import activity
from random import randint
import asyncio

from models import AppSubmittion

@activity.defn
async def run_credit_check(submittion: AppSubmittion):
    await asyncio.sleep(1)
    credit = randint(0, int(7*submittion.income))

    if (credit < 100) and (credit % 2 == 0):
        raise Exception("404 error")

    return credit

@activity.defn
async def calculate_risk_score():
    await asyncio.sleep(15)
    
    risk_score = randint(40,70)

    if risk_score < 40:
        return (risk_score, "auto-reject")
    if 40 <= risk_score <= 70:
        return (risk_score, "manual_review")
    return (risk_score, "auto-approve")