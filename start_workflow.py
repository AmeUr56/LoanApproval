import asyncio
from temporalio.client import Client

from workflows import AutoLoanApprovalWorkflow, ManualReviewWorkflow
from models import AppSubmittion

async def main():
    client = await Client.connect("127.0.0.1:7233")
    payload = AppSubmittion(
        application_id="124",
        income=30000,
        loan_amount=9000
    )
    result = await client.start_workflow(
        AutoLoanApprovalWorkflow.run,
        payload,
        id=f"auto-loan-{payload.application_id}",
        task_queue="auto_loan_approver_queue",
    )


if __name__ == "__main__":
    asyncio.run(main())
