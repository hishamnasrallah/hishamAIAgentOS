# HishamOS - Business Analyst Agent & Auto Story Generation
## من الفكرة الغامضة إلى Full Project Scope تلقائياً

---

# 🎯 Overview

نظام شامل يحول **أي فكرة مشروع** مهما كانت غامضة إلى:
- ✅ Full Scope Document
- ✅ Full SRS (Software Requirements Specification)
- ✅ Full BRD (Business Requirements Document)
- ✅ Full User Stories جاهزة للتنفيذ
- ✅ **أتمتة كاملة** من الفكرة → الكود

---

# 🤖 Business Analyst (BA) Agent

## Agent Configuration

```python
BA_AGENT = {
    "agent_id": "agent_ba_001",
    "name": "Business Analyst Agent",
    "type": "requirements_specialist",
    "primary_role": "Requirements Elicitation & Analysis",
    "capabilities": [
        "requirements_extraction",
        "stakeholder_interview",
        "scope_definition",
        "user_story_generation",
        "srs_writing",
        "brd_creation",
        "use_case_modeling",
        "process_mapping"
    ],
    "models": {
        "primary": "gpt-4",
        "fallback": "claude-3-sonnet"
    }
}
```

## System Prompt

```
# ROLE: Expert Business Analyst & Requirements Engineer

You are an AI-powered Business Analyst with 15+ years of experience in:
- Requirements elicitation and analysis
- Software project scoping
- User story creation
- Business process modeling
- Stakeholder management

## YOUR MISSION:
Transform vague project ideas into detailed, actionable requirements documents.

## CORE CAPABILITIES:

### 1. REQUIREMENTS ELICITATION
**Technique**: Socratic Questioning Method
- Ask probing questions to uncover hidden requirements
- Challenge assumptions
- Identify gaps and inconsistencies
- Extract both functional and non-functional requirements

**Interview Strategy**:
1. **Understand the Vision**
   - What problem are you solving?
   - Who are the users?
   - What's the desired outcome?

2. **Define the Scope**
   - What's in scope?
   - What's out of scope?
   - What are the constraints?

3. **Detail the Requirements**
   - What features are needed?
   - What workflows are involved?
   - What are the business rules?

4. **Identify Non-Functional Requirements**
   - Performance expectations?
   - Security requirements?
   - Scalability needs?
   - Compliance requirements?

### 2. DOCUMENT CREATION

**You MUST produce**:

#### A. Project Scope Document
```markdown
# Project Scope: [Project Name]

## 1. Executive Summary
[2-3 paragraph overview]

## 2. Project Objectives
- Objective 1
- Objective 2
- ...

## 3. In-Scope Items
- Feature A
- Feature B
- ...

## 4. Out-of-Scope Items
- Item X
- Item Y
- ...

## 5. Success Criteria
- Criterion 1
- Criterion 2
- ...

## 6. Assumptions & Constraints
**Assumptions**:
- Assumption 1
- ...

**Constraints**:
- Constraint 1
- ...

## 7. Stakeholders
| Role | Name | Responsibilities |
|------|------|-----------------|
| ... | ... | ... |
```

#### B. Software Requirements Specification (SRS)
```markdown
# SRS: [Project Name]

## 1. Introduction
### 1.1 Purpose
### 1.2 Scope
### 1.3 Definitions & Acronyms
### 1.4 References

## 2. Overall Description
### 2.1 Product Perspective
### 2.2 Product Features
### 2.3 User Classes
### 2.4 Operating Environment
### 2.5 Design & Implementation Constraints
### 2.6 Assumptions & Dependencies

## 3. Functional Requirements
### 3.1 Feature 1
**Description**: ...
**Priority**: High/Medium/Low
**User Story**: As a [user], I want [feature], so that [benefit]
**Acceptance Criteria**:
- Criterion 1
- Criterion 2

### 3.2 Feature 2
[repeat...]

## 4. Non-Functional Requirements
### 4.1 Performance
### 4.2 Security
### 4.3 Usability
### 4.4 Reliability
### 4.5 Scalability

## 5. External Interfaces
### 5.1 User Interfaces
### 5.2 Hardware Interfaces
### 5.3 Software Interfaces
### 5.4 Communication Interfaces

## 6. Data Requirements
### 6.1 Data Models
### 6.2 Data Dictionary
```

#### C. Business Requirements Document (BRD)
```markdown
# BRD: [Project Name]

## 1. Business Objectives
## 2. Current Business Process
## 3. Proposed Business Process
## 4. Business Rules
## 5. ROI Analysis
## 6. Risk Assessment
```

### 3. USER STORY GENERATION

**Format** (strict adherence):
```
As a [user role],
I want [feature/functionality],
So that [business value/benefit].

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Priority**: [Critical/High/Medium/Low]
**Story Points**: [1/2/3/5/8/13]
**Dependencies**: [List of dependent stories]
**Technical Notes**: [Any technical considerations]
```

**Story Decomposition Rules**:
1. Each story should be INVEST compliant:
   - **I**ndependent
   - **N**egotiable
   - **V**aluable
   - **E**stimable
   - **S**mall
   - **T**estable

2. Break large epics into smaller stories
3. Identify dependencies
4. Prioritize using MoSCoW method (Must/Should/Could/Won't)

### 4. QUALITY STANDARDS

**Every document must**:
- Be clear and unambiguous
- Be complete (no "TBD" unless explicitly required)
- Be consistent across all documents
- Be verifiable (measurable acceptance criteria)
- Follow industry best practices (IEEE 830 for SRS)

### 5. INTERACTIVE ELICITATION

When given a vague idea, use this conversation flow:

**Phase 1: Understanding (5-10 questions)**
```
Q1: What is the main problem this project solves?
Q2: Who are the primary users?
Q3: What does success look like?
Q4: What similar solutions exist? What makes yours different?
Q5: What is your timeline and budget?
```

**Phase 2: Deep Dive (10-20 questions)**
```
Q1: Walk me through a typical user journey
Q2: What are the key features? Rank them by importance
Q3: What data will the system handle?
Q4: What integrations are needed?
Q5: What are the security requirements?
Q6: What are the performance expectations?
...
```

**Phase 3: Clarification (5-10 questions)**
```
Q1: I understand you need [X]. What happens if [edge case]?
Q2: You mentioned [Y]. Does this mean [interpretation]?
Q3: How should the system handle [scenario]?
...
```

**Phase 4: Confirmation**
```
Let me summarize what I've understood:
[Full summary of requirements]

Is this accurate? Any corrections or additions?
```

### 6. OUTPUT FORMAT

Always structure your response as:

```json
{
  "phase": "understanding|deep_dive|clarification|documentation",
  "questions": [...],
  "insights": [...],
  "documents": {
    "scope": "...",
    "srs": "...",
    "brd": "...",
    "user_stories": [...]
  },
  "next_steps": [...]
}
```

## REMEMBER:
- Be thorough but efficient
- Ask smart, targeted questions
- Challenge assumptions politely
- Think like both a business analyst AND a software architect
- Your goal: transform vagueness into clarity
```

---

# 🔄 Requirements Elicitation Workflow

## Phase 1: Initial Intake

```python
class RequirementsElicitationEngine:
    """
    محرك استخراج المتطلبات التفاعلي
    """
    
    async def start_elicitation_session(
        self,
        user_id: str,
        initial_idea: str
    ) -> str:
        """
        بدء جلسة استخراج متطلبات
        """
        # Create session
        session = {
            'user_id': user_id,
            'initial_idea': initial_idea,
            'phase': 'understanding',
            'questions_asked': [],
            'answers_collected': [],
            'requirements': {},
            'created_at': datetime.utcnow()
        }
        
        session_id = await db.elicitation_sessions.create(session)
        
        # Get first set of questions from BA Agent
        questions = await self._get_phase_questions(
            session_id,
            'understanding',
            initial_idea
        )
        
        return {
            'session_id': session_id,
            'phase': 'understanding',
            'message': 'Great! Let me ask you some questions to understand your vision better.',
            'questions': questions
        }
    
    async def _get_phase_questions(
        self,
        session_id: str,
        phase: str,
        context: str
    ) -> List[str]:
        """
        الحصول على أسئلة المرحلة الحالية
        """
        prompt = f"""
        Based on this project idea:
        "{context}"
        
        We are in the {phase} phase of requirements elicitation.
        
        Generate 5-10 targeted questions to understand:
        - User needs
        - Business objectives
        - Technical constraints
        - Scope boundaries
        
        Return as JSON array of questions.
        """
        
        response = await ba_agent.execute(
            command='generate_elicitation_questions',
            input_data={'prompt': prompt}
        )
        
        return json.loads(response['content'])['questions']
    
    async def process_answers(
        self,
        session_id: str,
        answers: Dict[str, str]
    ):
        """
        معالجة إجابات المستخدم
        """
        session = await db.elicitation_sessions.get(session_id)
        
        # Store answers
        session['answers_collected'].extend([
            {'question': q, 'answer': a}
            for q, a in answers.items()
        ])
        
        await db.elicitation_sessions.update(session_id, session)
        
        # Determine next phase
        next_phase = await self._determine_next_phase(session)
        
        if next_phase == 'complete':
            # Generate documents
            return await self.generate_requirements_documents(session_id)
        else:
            # Get next questions
            questions = await self._get_phase_questions(
                session_id,
                next_phase,
                self._build_context_from_answers(session)
            )
            
            return {
                'session_id': session_id,
                'phase': next_phase,
                'questions': questions
            }
    
    async def generate_requirements_documents(
        self,
        session_id: str
    ) -> Dict:
        """
        توليد جميع وثائق المتطلبات
        """
        session = await db.elicitation_sessions.get(session_id)
        
        # Build comprehensive context
        context = self._build_full_context(session)
        
        # Generate Scope Document
        scope_doc = await ba_agent.execute(
            command='generate_scope_document',
            input_data={'context': context}
        )
        
        # Generate SRS
        srs_doc = await ba_agent.execute(
            command='generate_srs',
            input_data={'context': context}
        )
        
        # Generate BRD
        brd_doc = await ba_agent.execute(
            command='generate_brd',
            input_data={'context': context}
        )
        
        # Generate User Stories
        user_stories = await self.generate_user_stories(session_id)
        
        # Store documents
        docs = {
            'scope': scope_doc['content'],
            'srs': srs_doc['content'],
            'brd': brd_doc['content'],
            'user_stories': user_stories
        }
        
        await db.elicitation_sessions.update(
            session_id,
            {
                'phase': 'complete',
                'documents': docs,
                'completed_at': datetime.utcnow()
            }
        )
        
        return docs
```

---

# 📝 Auto User Stories Generation

## Story Generation Engine

```python
class AutoStoryGenerator:
    """
    مولد User Stories تلقائي
    """
    
    async def generate_user_stories(
        self,
        session_id: str
    ) -> List[Dict]:
        """
        توليد User Stories من المتطلبات
        """
        session = await db.elicitation_sessions.get(session_id)
        
        # Build context from all collected requirements
        requirements_context = self._extract_requirements(session)
        
        # Use BA Agent to generate stories
        prompt = f"""
        Based on these comprehensive requirements:
        
        {json.dumps(requirements_context, indent=2)}
        
        Generate a complete set of user stories organized by Epic.
        
        For each Epic:
        1. Epic title and description
        2. List of user stories
        
        For each User Story:
        - Follow format: "As a [role], I want [feature], so that [benefit]"
        - Include detailed acceptance criteria
        - Assign priority (Critical/High/Medium/Low)
        - Estimate story points (1/2/3/5/8/13)
        - Identify dependencies
        - Add technical notes
        
        Ensure stories are INVEST compliant:
        - Independent
        - Negotiable
        - Valuable
        - Estimable
        - Small
        - Testable
        
        Return as structured JSON.
        """
        
        response = await ba_agent.execute(
            command='generate_user_stories',
            input_data={'prompt': prompt}
        )
        
        stories_data = json.loads(response['content'])
        
        # Process and store stories
        all_stories = []
        
        for epic in stories_data['epics']:
            # Create Epic
            epic_id = await self._create_epic(session_id, epic)
            
            # Create Stories
            for story_data in epic['stories']:
                story = await self._create_story(
                    session_id,
                    epic_id,
                    story_data
                )
                all_stories.append(story)
        
        return all_stories
    
    async def _create_epic(
        self,
        session_id: str,
        epic_data: Dict
    ) -> str:
        """
        إنشاء Epic
        """
        session = await db.elicitation_sessions.get(session_id)
        
        epic = {
            'session_id': session_id,
            'title': epic_data['title'],
            'description': epic_data['description'],
            'business_value': epic_data['business_value'],
            'priority': epic_data['priority'],
            'status': 'defined'
        }
        
        epic_id = await db.epics.create(epic)
        return epic_id
    
    async def _create_story(
        self,
        session_id: str,
        epic_id: str,
        story_data: Dict
    ) -> Dict:
        """
        إنشاء User Story
        """
        story = {
            'session_id': session_id,
            'epic_id': epic_id,
            'title': story_data['title'],
            'user_role': story_data['user_role'],
            'feature': story_data['feature'],
            'benefit': story_data['benefit'],
            'acceptance_criteria': story_data['acceptance_criteria'],
            'priority': story_data['priority'],
            'story_points': story_data['story_points'],
            'dependencies': story_data.get('dependencies', []),
            'technical_notes': story_data.get('technical_notes', ''),
            'status': 'ready'
        }
        
        story_id = await db.user_stories.create(story)
        
        return {
            'id': story_id,
            **story
        }
    
    async def auto_create_project_from_stories(
        self,
        session_id: str,
        project_name: str,
        project_key: str
    ) -> str:
        """
        إنشاء مشروع كامل من User Stories
        """
        # Get all stories
        stories = await db.user_stories.find({'session_id': session_id})
        
        # Create project
        project = {
            'project_key': project_key,
            'name': project_name,
            'description': f'Auto-generated from requirements session {session_id}',
            'ai_enabled': True,
            'status': 'active'
        }
        
        project_id = await db.projects.create(project)
        
        # Create initial sprint
        sprint = {
            'project_id': project_id,
            'sprint_number': 1,
            'name': 'Sprint 1 - Foundation',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=14),
            'status': 'planned'
        }
        
        sprint_id = await db.sprints.create(sprint)
        
        # Convert user stories to project stories
        for story in stories:
            project_story = {
                'project_id': project_id,
                'sprint_id': sprint_id if story['priority'] in ['Critical', 'High'] else None,
                'story_key': f"{project_key}-{len(stories) + 1}",
                'title': story['title'],
                'description': self._format_story_description(story),
                'story_type': 'story',
                'priority': story['priority'].lower(),
                'story_points': story['story_points'],
                'assigned_to_ai': True,  # Ready for AI execution
                'status': 'todo',
                'board_column': 'Todo'
            }
            
            await db.stories.create(project_story)
        
        return project_id
```

---

# 🎨 UI Design - Requirements Elicitation

## Interactive Wizard

```
┌────────────────────────────────────────────────────────────────┐
│ 🧠 Business Analyst - Requirements Elicitation                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase: Understanding Your Vision         [Progress: 1/4 ██░░] │
│                                                                 │
│  Tell me about your project idea:                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ I want to build a task management app for remote teams   │ │
│  │ that helps them collaborate better...                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Great! Let me ask you some questions:                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Q1: Who are the primary users of this app?               │ │
│  │ [ Remote team members, project managers, executives  ]   │ │
│  │                                                           │ │
│  │ Q2: What's the main problem they face currently?         │ │
│  │ [ Lack of visibility, scattered communication...     ]   │ │
│  │                                                           │ │
│  │ Q3: How many users do you expect initially?              │ │
│  │ ( ) 1-50  (•) 50-200  ( ) 200-1000  ( ) 1000+           │ │
│  │                                                           │ │
│  │ Q4: Do you have any existing systems to integrate with?  │ │
│  │ [✓] Slack  [✓] Jira  [ ] Teams  [ ] Other            │ │
│  │                                                           │ │
│  │ Q5: What's your launch timeline?                          │ │
│  │ ( ) 1-3 months  (•) 3-6 months  ( ) 6-12 months         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [Back]  [Save Draft]  [Continue to Next Phase]               │
└────────────────────────────────────────────────────────────────┘
```

## Generated Documents View

```
┌────────────────────────────────────────────────────────────────┐
│ 📋 Generated Requirements Documents                     [Export]│
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Session completed! Here are your documents:                   │
│                                                                 │
│  ┌─ 📄 Project Scope Document ─────────────────────────────┐  │
│  │ ▼ Executive Summary                                      │  │
│  │   [Generated 3-paragraph summary...]                     │  │
│  │                                                           │  │
│  │ ▼ Objectives (5)                                         │  │
│  │   ✓ Enable real-time collaboration                       │  │
│  │   ✓ Integrate with existing tools                        │  │
│  │   ...                                                     │  │
│  │                                                           │  │
│  │ ▼ In-Scope (12 items)                                    │  │
│  │ ▼ Out-of-Scope (5 items)                                │  │
│  │ ▼ Success Criteria (6 items)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ 📘 Software Requirements Specification (SRS) ─────────┐  │
│  │ 45 pages | 67 functional requirements | 23 non-functional│  │
│  │ [View Full SRS →]                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ 📗 Business Requirements Document (BRD) ──────────────┐  │
│  │ 28 pages | ROI Analysis | Risk Assessment               │  │
│  │ [View Full BRD →]                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ 📝 User Stories (Generated: 52 stories) ─────────────┐  │
│  │                                                           │  │
│  │ Epic 1: User Management (8 stories)                     │  │
│  │   TASK-1: As an admin, I want to...        [High] [5pts]│  │
│  │   TASK-2: As a user, I want to...          [Med]  [3pts]│  │
│  │   ...                                                     │  │
│  │                                                           │  │
│  │ Epic 2: Task Management (12 stories)                    │  │
│  │ Epic 3: Collaboration Features (15 stories)             │  │
│  │ Epic 4: Reporting & Analytics (9 stories)               │  │
│  │ Epic 5: Integration (8 stories)                          │  │
│  │                                                           │  │
│  │ [View All Stories →]                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  🚀 Next Steps:                                                │
│  [ ] Review & Approve Documents                                │
│  [ ] Create Project from Stories                               │
│  [ ] Start AI Auto-Execution                                   │
│                                                                 │
│  [Export All]  [Create Project]  [🤖 Auto-Execute Everything] │
└────────────────────────────────────────────────────────────────┘
```

---

# 🔄 Complete Automation Flow

## Idea → Production (Fully Automated)

```
Vague Idea
    ↓
BA Agent Interactive Session
    ↓
    ├─ Scope Document
    ├─ SRS
    ├─ BRD
    └─ User Stories (52 stories)
        ↓
Auto-Create Project
    ├─ Create Project
    ├─ Create Sprints
    └─ Import Stories
        ↓
Auto-Execute with AI
    ├─ Story 1 → AI executes → Dev → Review → Test → QA → Done
    ├─ Story 2 → AI executes → Dev → Review → Test → QA → Done
    └─ ... (all stories)
        ↓
Full Application Ready
```

---

# 📊 Database Schema Updates

```sql
-- Requirements Elicitation Sessions
CREATE TABLE elicitation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    initial_idea TEXT NOT NULL,
    phase VARCHAR(50) DEFAULT 'understanding',
    questions_asked JSONB DEFAULT '[]',
    answers_collected JSONB DEFAULT '[]',
    requirements JSONB DEFAULT '{}',
    documents JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Epics
CREATE TABLE epics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES elicitation_sessions(id),
    project_id UUID REFERENCES projects(id),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    business_value TEXT,
    priority VARCHAR(20),
    status VARCHAR(50) DEFAULT 'defined',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Stories (template before project creation)
CREATE TABLE user_stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES elicitation_sessions(id),
    epic_id UUID REFERENCES epics(id),
    title VARCHAR(500) NOT NULL,
    user_role VARCHAR(100),
    feature TEXT,
    benefit TEXT,
    acceptance_criteria JSONB DEFAULT '[]',
    priority VARCHAR(20),
    story_points INTEGER,
    dependencies JSONB DEFAULT '[]',
    technical_notes TEXT,
    status VARCHAR(50) DEFAULT 'ready',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# ✅ Summary - الخلاصة

## ✨ ما تمت إضافته:

### 1. **Business Analyst (BA) Agent** ⭐
- خبير استخراج متطلبات
- يطرح أسئلة ذكية
- يحول الأفكار الغامضة → متطلبات واضحة

### 2. **Requirements Elicitation System**
- جلسات تفاعلية
- 4 مراحل (Understanding → Deep Dive → Clarification → Documentation)
- أسئلة مستهدفة

### 3. **Auto Document Generation**
- ✅ Project Scope
- ✅ Full SRS (Software Requirements Specification)
- ✅ Full BRD (Business Requirements Document)

### 4. **Auto User Stories Generation**
- توليد تلقائي من المتطلبات
- INVEST-compliant
- مع Acceptance Criteria
- Story Points تلقائية

### 5. **Full Automation** 🚀
- Idea → Documents → Stories → Project → AI Execution → Done
- **أتمتة كاملة 100%**

---

## 🎯 الآن HishamOS يستطيع:

1. ✅ **استخراج المتطلبات** من أي فكرة غامضة
2. ✅ **توليد Full Scope, SRS, BRD** تلقائياً
3. ✅ **إنشاء User Stories** تلقائياً
4. ✅ **بناء المشروع** تلقائياً
5. ✅ **تنفيذ جميع Stories** بالذكاء الاصطناعي
6. ✅ **إنجاز المشروع كاملاً** من الفكرة → الكود

**من الفكرة إلى المنتج النهائي - بدون تدخل بشري!** 🚀
