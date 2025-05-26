from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from medical_report_generator.tools import MedicalReportClassifierTool, RAGMedicalReportsTool


@CrewBase
class MedicalReportGenerator:
    """MedicalReportGenerator crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    knowledge_base_path = "knowledge/reports/training"

    @agent
    def report_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config["report_classifier"],
            tools=[MedicalReportClassifierTool()],
            verbose=True,
        )

    @agent
    def information_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config["information_extractor"],
            tools=[RAGMedicalReportsTool(knowledge_base_path=self.knowledge_base_path)],
            verbose=True,
        )

    @agent
    def template_mapper(self) -> Agent:
        return Agent(
            config=self.agents_config["template_mapper"],
            tools=[RAGMedicalReportsTool(knowledge_base_path=self.knowledge_base_path)],
            verbose=True,
        )

    @agent
    def report_section_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["report_section_generator"],
            tools=[RAGMedicalReportsTool(knowledge_base_path=self.knowledge_base_path)],
            verbose=True,
        )

    @agent
    def semantic_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["semantic_validator"],
            verbose=True,
        )

    @agent
    def report_finalizer_and_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["report_finalizer_and_reviewer"],
            verbose=True,
        )

    @task
    def determine_report_type(self) -> Task:
        return Task(
            config=self.tasks_config["determine_report_type"],
            agent=self.report_classifier(),
        )

    @task
    def retrieve_medical_info(self) -> Task:
        return Task(
            config=self.tasks_config["retrieve_medical_info"],
            agent=self.information_extractor(),
            context=[self.determine_report_type()],
        )


    @task
    def organize_into_sections(self) -> Task:
        return Task(
            config=self.tasks_config["organize_into_sections"],
            agent=self.template_mapper(),
        )

    @task
    def compose_section_text(self) -> Task:
        return Task(
            config=self.tasks_config["compose_section_text"],
            agent=self.report_section_generator(),
            context=[self.organize_into_sections()],
        )

    @task
    def check_semantic_coherence(self) -> Task:
        return Task(
            config=self.tasks_config["check_semantic_coherence"],
            agent=self.semantic_validator(),
            context=[self.compose_section_text()],
        )

    @task
    def compile_finalize_report(self) -> Task:
        return Task(
            config=self.tasks_config["compile_finalize_report"],
            agent=self.report_finalizer_and_reviewer(),
            context=[
                self.check_semantic_coherence(),
                self.determine_report_type(),
            ],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MedicalReportGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=[
                self.determine_report_type(),
                self.retrieve_medical_info(),
                self.organize_into_sections(),
                self.compose_section_text(),
                self.check_semantic_coherence(),
                self.compile_finalize_report(),
            ],
            process=Process.sequential,
            verbose=True,
        )
