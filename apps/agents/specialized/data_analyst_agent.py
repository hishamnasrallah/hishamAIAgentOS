from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class DataAnalystAgent(BaseAgent):
    """
    Data Analyst Agent
    Specialized in data analysis, insights generation, and reporting.
    """

    agent_type = AgentType.DATA_ANALYST
    agent_name = "Data Analyst Agent"
    agent_description = "Expert in data analysis and insights generation"
    capabilities = [
        "DATA_ANALYSIS",
        "STATISTICAL_ANALYSIS",
        "VISUALIZATION_DESIGN",
        "REPORTING",
        "INSIGHTS_GENERATION"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Data Analyst task.

        Expected input_data:
            - task_type: ANALYZE | VISUALIZE | REPORT | INSIGHTS | METRICS
            - data: Data to analyze
            - question: Analysis question
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'ANALYZE')
        data = input_data.get('data', '')
        question = input_data.get('question', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Data Analyst task: {task_type}")

        user_message = self._build_analyst_prompt(task_type, data, question, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'analysis': response
        }

    def _build_analyst_prompt(
        self,
        task_type: str,
        data: str,
        question: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for data analyst task."""

        if task_type == 'ANALYZE':
            return f"""
I need you to analyze this data.

{f"Question:\n{question}\n" if question else ""}

Data:
{data}

Please provide comprehensive analysis:

1. **Data Overview** 📊
   - Data structure
   - Data types
   - Data quality assessment
   - Missing values
   - Outliers

2. **Descriptive Statistics** 📈
   - Mean, median, mode
   - Standard deviation
   - Min, max, range
   - Quartiles
   - Distribution

3. **Data Patterns** 🔍
   - Trends identified
   - Correlations
   - Anomalies
   - Seasonality (if applicable)

4. **Segmentation** 📑
   - Key segments identified
   - Segment characteristics
   - Segment comparison

5. **Statistical Tests** 🧪
   - Hypothesis testing (if applicable)
   - Significance tests
   - Confidence intervals

6. **Key Findings** 💡
   - Most important insights
   - Unexpected discoveries
   - Data-driven conclusions

7. **Recommendations** 🎯
   - Actionable recommendations
   - Based on data evidence
   - Prioritized by impact

8. **Further Analysis** 🔬
   - Additional questions to explore
   - Data needed
   - Analysis methods to apply

Context: {context if context else 'None'}
"""

        elif task_type == 'VISUALIZE':
            return f"""
I need you to design data visualizations.

Data:
{data}

{f"Question:\n{question}\n" if question else ""}

Please recommend visualizations:

1. **Visualization Strategy** 📊
   - What story to tell
   - Key messages
   - Target audience

2. **Chart Recommendations** 📈
   For each visualization:

   **Chart 1**: [Type]
   - Purpose: What it shows
   - Data fields: X-axis, Y-axis, etc.
   - Why this chart type?
   - Insights to highlight

   **Chart 2**: [Type]
   ...

3. **Chart Types to Use** 📉
   - Line chart: For trends over time
   - Bar chart: For comparisons
   - Pie chart: For proportions
   - Scatter plot: For correlations
   - Heatmap: For patterns
   - Histogram: For distributions

4. **Dashboard Design** 🖥️
   - Layout structure
   - Chart arrangement
   - Filters needed
   - Interactive elements

5. **Design Guidelines** 🎨
   - Color palette
   - Typography
   - Legend placement
   - Annotations
   - Responsive design

6. **Implementation** 💻
   - Tool recommendations (Chart.js, D3.js, etc.)
   - Code structure
   - Data format

Context: {context if context else 'None'}
"""

        elif task_type == 'REPORT':
            return f"""
I need you to create a data report.

Data:
{data}

{f"Focus:\n{question}\n" if question else ""}

Please create a comprehensive report:

# Data Analysis Report

## Executive Summary 📋
- Key findings (3-5 bullet points)
- Main recommendations
- Impact assessment

## Introduction 📖
- Report purpose
- Data sources
- Analysis period
- Methodology

## Data Overview 📊
- Dataset description
- Data quality
- Limitations

## Analysis 🔍

### Key Metrics
- Metric 1: Value (trend)
- Metric 2: Value (trend)
- Metric 3: Value (trend)

### Detailed Findings
1. **Finding 1**
   - Description
   - Supporting data
   - Implications

2. **Finding 2**
   - Description
   - Supporting data
   - Implications

### Trends & Patterns 📈
- Trend 1
- Trend 2
- Pattern analysis

### Comparisons ⚖️
- Period over period
- Segment comparison
- Benchmark comparison

## Insights 💡
- Key insights discovered
- Unexpected findings
- Correlations identified

## Recommendations 🎯
1. **Recommendation 1**
   - Action: What to do
   - Impact: Expected outcome
   - Priority: High/Medium/Low

2. **Recommendation 2**
   ...

## Conclusion 🎓
- Summary
- Next steps
- Success metrics

## Appendix 📎
- Methodology details
- Data dictionary
- Additional charts

Context: {context if context else 'None'}
"""

        elif task_type == 'INSIGHTS':
            return f"""
I need you to extract insights from this data.

Data:
{data}

{f"Focus Area:\n{question}\n" if question else ""}

Please provide actionable insights:

1. **Top Insights** 💡

   **Insight 1**: [Title]
   - What: What the data shows
   - So What: Why it matters
   - Now What: What action to take
   - Impact: Expected outcome
   - Confidence: High/Medium/Low

   **Insight 2**: [Title]
   ...

   **Insight 3**: [Title]
   ...

2. **Surprising Discoveries** 🔎
   - Unexpected patterns
   - Anomalies explained
   - Counterintuitive findings

3. **Opportunity Analysis** 🚀
   - Growth opportunities
   - Quick wins
   - Long-term opportunities
   - Market gaps

4. **Risk Identification** ⚠️
   - Risks spotted in data
   - Warning signs
   - Mitigation strategies

5. **Competitive Intelligence** 🎯
   - Competitive advantages
   - Market position
   - Differentiation opportunities

6. **Predictive Insights** 🔮
   - Future trends
   - Projections
   - Scenario analysis

7. **Actionable Recommendations** ✅
   - Prioritized actions
   - Expected ROI
   - Implementation roadmap

Context: {context if context else 'None'}
"""

        elif task_type == 'METRICS':
            return f"""
I need help defining metrics and KPIs.

Context:
{question}

{f"Current Data:\n{data}\n" if data else ""}

Please provide a comprehensive metrics framework:

1. **North Star Metric** ⭐
   - The ONE metric that matters most
   - Why this metric?
   - How to measure it

2. **Primary KPIs** 📊
   For each KPI:

   **KPI 1**: [Name]
   - Definition: What it measures
   - Formula: How to calculate
   - Target: Goal value
   - Frequency: How often to measure
   - Owner: Who tracks it

   **KPI 2**: [Name]
   ...

3. **Secondary Metrics** 📈
   - Supporting metrics
   - Leading indicators
   - Lagging indicators

4. **Metric Categories** 📑
   - Acquisition metrics
   - Engagement metrics
   - Retention metrics
   - Revenue metrics
   - Operational metrics

5. **Dashboard Design** 🖥️
   - Metrics to display
   - Visualization types
   - Update frequency
   - Alert thresholds

6. **Measurement Plan** 📋
   - Data sources
   - Collection methods
   - Calculation logic
   - Quality checks

7. **Success Criteria** ✅
   - What success looks like
   - Targets and goals
   - Review cadence

Context: {context if context else 'None'}
"""

        else:
            return data or question
