# MedicalReportGenerator Crew

Welcome to the MedicalReportGenerator Crew, an advanced AI-based system designed to generate formal medical reports from raw clinical notes and dictations in French. This project is powered by [crewAI](https://crewai.com), a framework for creating multi-agent AI systems that collaborate effectively on complex tasks.

## Project Overview

This system uses a team of specialized AI agents working together to transform unstructured French medical text into properly formatted radiology reports using a standardized Word document template.

### AI Agent Workflow

1. **Report Classifier (`report_classifier`)**: Identifies the specific type of medical examination (e.g., IRM du genou, IRM hépatique) from the input text. Its output is used for dynamic report titling and to guide focused RAG retrieval.

2. **Information Extractor (`information_extractor`)**: Identifies and extracts all relevant medical facts from the raw input, utilizing a RAG (Retrieval Augmented Generation) tool that can leverage similar reports from a knowledge base, filtered by the classified report type.

3. **Template Mapper (`template_mapper`)**: Maps extracted data to appropriate sections of a standard French radiology report (Indication, Technique, Incidences, Résultat, Conclusion).

4. **Report Section Generator (`report_section_generator`)**: Transforms the structured data for each section into professional medical language, in French.

5. **Semantic Validator (`semantic_validator`)**: Reviews the generated section content for clinical and semantic coherence, checking for contradictions or medically improbable statements, and suggests corrections if needed.

6. **Report Finalizer and Reviewer (`report_finalizer_and_reviewer`)**: Assembles the validated sections into the final report structure using a predefined Word template. It uses the classified report type to generate a dynamic title and ensures empty sections are appropriately marked.

The system outputs a professional radiology report in French as a formatted Word document (.docx).

## Key Features

- **Multi-Agent System**: Leverages multiple specialized AI agents for a modular and robust workflow
- **French Language Focus**: All agents, tasks, and tools are configured to process and generate medical reports in French
- **Enhanced Information Extraction**: The system attempts to identify and extract patient age and sex from the input prompt, integrating this information into the "Indication" section
- **Dynamic Report Titling**: The title of the generated report is dynamically set based on the type of medical examination identified
- **Retrieval Augmented Generation (RAG)**: Uses a knowledge base of existing French medical reports to improve generation quality through similar report retrieval
- **Report Type Classification**: Dedicated classification tool uses keyword matching to identify specific types of medical examinations
- **Semantic Validation**: Reviews drafted report sections for clinical and semantic consistency
- **Professional Word Document Output**: Generates formatted Word documents using predefined templates with proper section structure
- **Configurable Workflow**: Agents and tasks are defined in YAML files for easy customization

## Template Structure

The system uses a standardized Word document template with the following structure:

### Document Template Layout

![image](https://github.com/user-attachments/assets/e9c47cc8-5da6-4bd9-a508-4277562f762d)



The template includes:
- **Dynamic Title**: Generated based on examination type (e.g., "Compte Rendu IRM du Genou")
- **Indication**: Patient information, symptoms, and clinical context
- **Technique**: Technical details of the examination performed
- **Incidences**: Additional imaging planes or sequences (if applicable)
- **Résultat**: Detailed findings and observations
- **Conclusion**: Clinical interpretation and recommendations

Empty sections are automatically filled with "Néant" to maintain professional formatting.

## Input Data Processing

### Raw Medical Text Input

The system accepts unstructured French medical text including:
- Clinical notes and observations
- Patient history and symptoms
- Dictated reports from medical professionals
- Technical examination details

### Input Example

Example input format:
```
Patient de 45 ans, fumeur, adressé pour bilan d'une toux persistante depuis 2 mois avec dyspnée d'effort.
Antécédents : Tabagisme actif (30 paquets-années), HTA sous traitement.
Examen clinique : Toux sèche, dyspnée stade II, auscultation normale.
L'examen tomodensitométrique thoracique a été réalisé sans injection de produit de contraste, puis après injection intraveineuse de 100ml de produit de contraste iodé.
Résultats :
Parenchyme pulmonaire : Présence de multiples nodules pulmonaires bilatéraux, le plus volumineux au niveau du lobe supérieur droit mesurant 25mm de diamètre. Aspect hétérogène avec prise de contraste périphérique. Quelques nodules satellites de plus petite taille (5-8mm).
Plèvre : Épanchement pleural de faible abondance bilatéral, prédominant à droite.
Médiastin : Présence d'adénopathies médiastinales, notamment au niveau de la fenêtre aorto-pulmonaire et des régions hilaires bilatérales. La plus volumineuse mesure 18mm.
Paroi thoracique : Sans particularité.
Structures vasculaires : Aorte et artères pulmonaires de calibre normal.
Conclusion : Multiples nodules pulmonaires avec adénopathies médiastinales évocateurs de néoplasie broncho-pulmonaire primitive avec dissémination secondaire. Complément par biopsie bronchique recommandé.
```

The system automatically:
- Extracts patient demographics (age, sex)
- Identifies examination type and body region
- Categorizes clinical findings and technical details
- Maps information to appropriate report sections

## Output Generation

### Generated Report Structure

The system produces professionally formatted Word documents with:
- Consistent section headers and formatting
- Medical terminology in proper French
- Structured layout following radiology standards
- Dynamic titles based on examination type

### Output Example


Example generated report:

![image](https://github.com/user-attachments/assets/8d872dd8-eda7-441d-aba3-99e7bdbb546b)



## Requirements

- Python >=3.10 <3.13
- [UV](https://docs.astral.sh/uv/) for dependency management
- Google AI Studio account with API Key (uses Gemini 2.0 flash model)

## Installation

1. Ensure you have Python >=3.10 <3.13 installed on your system

2. Install UV (if not already installed):
```bash
pip install uv
```

3. Clone the repository and navigate to the project directory

4. Install dependencies:
```bash
crewai install
```

## Configuration Setup

1. Create a `.env` file in the project root based on the provided `.env.example`:
```bash
cp .env.exemple .env
```

2. Add your **Gemini API Key** to the `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can obtain a token from your [Google AI Studio account](https://aistudio.google.com/apikey).

## Running the Project

Run the medical report generator from the root folder of your project:

```bash
crewai run
```

This will:
1. Initialize all the AI agents
2. Process the sample French medical text in `main.py`
3. Generate a structured French radiology report
4. Create a formatted `.docx` file (e.g., `radiology_report.docx`)

## Customizing the Project

### Input Medical Text

Modify the `raw_medical_input` variable in `src/medical_report_generator/main.py` to process your own medical text.

### Knowledge Base (for RAG)

Place your French example medical reports (as `.txt` files) in `knowledge/reports/training/`. These are used by the `RAGMedicalReportsTool` to improve report generation quality.

### Agent Configuration

Each agent can be customized in `src/medical_report_generator/config/agents.yaml`:
- Modify roles, goals, and backstories
- Change or configure the LLM models used

### Report Template & Task Workflow

The report structure and task descriptions are defined in `src/medical_report_generator/config/tasks.yaml`. You can modify:
- Section names and organization
- Expected data formats
- Report generation instructions

## Project Structure

```
medical_report_generator/
├── .env                  # Environment variables (GEMINI_API_KEY)
├── knowledge/
│   └── reports/
├── templates/
│   └── report_template.docx
├── input_data/
│   ├── abdominal_mri.txt
│   ├── brain_mri.txt
│   └── chest_ct.txt
├── pyproject.toml        # Project dependencies and configuration
├── README.md             # This documentation file
├── generated/            # Folder for generated report files
│   └── reports/          # Contains generated .docx files
├── src/
│   └── medical_report_generator/
│       ├── config/
│       │   ├── agents.yaml   # Agent definitions (French roles/goals)
│       │   └── tasks.yaml    # Task definitions (French descriptions)
│       ├── crew.py           # Crew and agent/task orchestration
│       ├── main.py           # Main execution script
│       └── tools/
│           ├── __init__.py
│           ├── classifier_tool.py # Report type classification
│           ├── rag_tool.py        # RAG implementation
│           └── custom_tool.py     # Custom tools placeholder
```

## How It Works

1. **Input Processing**: French raw medical text is analyzed and classified
2. **Knowledge Retrieval**: Similar reports are retrieved from the knowledge base using RAG
3. **Data Extraction**: Key clinical details are extracted and categorized
4. **Template Mapping**: Information is organized into standard report sections
5. **Content Generation**: Professional French medical language is generated for each section
6. **Semantic Validation**: Generated content is reviewed for clinical coherence
7. **Final Assembly**: Sections are assembled into a complete report with dynamic titling
8. **Document Creation**: A formatted Word document is generated using the template structure

## Troubleshooting

- **Model Access Issues**: Ensure your Gemini API key has permission to access the model
- **Python Version Errors**: Verify you're using Python >=3.10 <3.13
- **Document Generation Errors**: Check that python-docx is properly installed

