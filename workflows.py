from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

from models import AppSubmittion, AppStatus
from activities import run_credit_check, calculate_risk_score

retry = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=60),
    maximum_attempts=5,
)


@workflow.defn
class ManualReviewWorkflow:
    def __init__(self):
        self.final_decision: str | None = None

    @workflow.run
    async def run(self):
        await workflow.wait_condition(
            lambda: self.final_decision is not None,
            timeout=timedelta(hours=24)
        )
        if self.final_decision is None:
            self.final_decision = "auto-reject"

    @workflow.signal
    async def approve(self):
        self.final_decision = "manual-approve"

    @workflow.signal
    async def reject(self):
        self.final_decision = "manual-reject"

    @workflow.query
    async def decision(self):
        return self.final_decision

@workflow.defn
class AutoLoanApprovalWorkflow:
    @workflow.run
    async def run(self, submittion: AppSubmittion):
        credit = await workflow.execute_activity(
            run_credit_check,
            submittion,
            retry_policy=retry,
            start_to_close_timeout=timedelta(seconds=30)
        )

        risk_score = await workflow.execute_activity(
            calculate_risk_score,
            retry_policy=retry,
            start_to_close_timeout=timedelta(seconds=30)
        )

        if risk_score[1] == "manual_review":
            await workflow.execute_child_workflow(
                ManualReviewWorkflow.run,
                id=f"manual-{submittion.application_id}"
            )
            decision = "manual"
        else:
            decision = risk_score[1]

        application_status = AppStatus(state="processed", risk_score=risk_score[0], decision=decision)

        return application_status