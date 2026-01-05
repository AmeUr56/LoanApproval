from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

from workflows import AutoLoanApprovalWorkflow, ManualReviewWorkflow
from activities import run_credit_check, calculate_risk_score

async def main():
    client = await Client.connect("127.0.0.1:7233")

    async with Worker(
        client,
        task_queue="auto_loan_approver_queue",
        workflows=[AutoLoanApprovalWorkflow, ManualReviewWorkflow],
        activities=[run_credit_check, calculate_risk_score]
    ):
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())