# Configuration file for the resume parser

# Model names
MODEL_NAME = "dslim/bert-large-NER"  # Better for general NER tasks

# Comprehensive skills database
skill_keywords = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "go", "kotlin",
    "typescript", "r", "scala", "perl", "bash", "html", "css", "sql", "dart", "rust",

    # Frameworks and Libraries
    "django", "flask", "react", "angular", "vue.js", "node.js", "spring", "laravel", "ruby on rails",
    "express.js", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
    "bootstrap", "jquery", "asp.net", "hadoop", "spark", "graphql", "redux", "flutter", "xamarin",

    # Tools and Platforms
    "git", "docker", "kubernetes", "jenkins", "ansible", "terraform", "aws", "azure", "google cloud",
    "heroku", "firebase", "tableau", "power bi", "splunk", "elasticsearch", "kibana", "grafana",
    "postgresql", "mysql", "mongodb", "oracle", "redis", "cassandra", "apache kafka", "rabbitmq",

    # Methodologies and Practices
    "agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "test-driven development", "unit testing",
    "integration testing", "api testing", "microservices", "restful apis", "graphql apis", "soa",
    "object-oriented programming", "oop", "functional programming", "design patterns", "data structures",
    "algorithms", "machine learning", "deep learning", "nlp", "natural language processing", "computer vision",
    "big data", "data mining", "data warehousing", "etl", "business intelligence", "cloud computing",

    # Soft Skills
    "communication", "teamwork", "problem-solving", "critical thinking", "time management",
    "leadership", "adaptability", "creativity", "collaboration", "emotional intelligence",
    "conflict resolution", "decision-making", "negotiation", "public speaking", "presentation",
    "mentoring", "project management", "stakeholder management", "strategic planning", "analytical thinking",

    # Other Technical Skills
    "linux", "windows", "macos", "shell scripting", "networking", "cybersecurity", "penetration testing",
    "blockchain", "smart contracts", "solidity", "web development", "mobile development", "ui/ux design",
    "game development", "embedded systems", "iot", "robotics", "arduino", "raspberry pi", "3d modeling",
    "cad", "gis", "quantum computing", "bioinformatics", "financial modeling", "risk management",
    "supply chain management", "logistics", "digital marketing", "seo", "content marketing", "social media marketing",
    "data visualization", "statistical analysis", "econometrics", "actuarial science", "quantitative analysis",

    # Data Science specific
    "data science", "data analysis", "statistical modeling", "feature engineering", "data cleansing",
    "data wrangling", "regression analysis", "classification", "clustering", "anomaly detection",
    "recommendation systems", "a/b testing", "hypothesis testing", "dimensionality reduction",
    "time series analysis", "forecasting", "bayesian methods", "neural networks", "sentiment analysis",
    "text mining", "reinforcement learning", "unsupervised learning", "supervised learning",
    "data preprocessing", "data pipelines", "data engineering", "exploratory data analysis", "eda"
]

# Common false positives in skill extraction
false_positives = [
    'university', 'company', 'corporation', 'inc', 'ltd', 'limited', 'international',
    'curriculum', 'vitae', 'resume', 'contact', 'profile', 'email', 'phone',
    'address', 'reference', 'recommendation'
]

# Skill section patterns for identification
skill_section_patterns = [
    r'(?i)SKILLS', r'(?i)TECHNICAL SKILLS', r'(?i)CORE COMPETENCIES', r'(?i)TECHNOLOGIES',
    r'(?i)TECHNICAL PROFICIENCIES', r'(?i)AREAS OF EXPERTISE', r'(?i)KEY SKILLS',
    r'(?i)PROFESSIONAL SKILLS', r'(?i)SKILL SET', r'(?i)TECHNICAL EXPERTISE',
    r'(?i)CORE SKILLS', r'(?i)QUALIFICATIONS', r'(?i)KEY COMPETENCIES',
    r'(?i)TECHNICAL KNOWLEDGE', r'(?i)PROFESSIONAL EXPERTISE'
]

# Location patterns for extraction
location_patterns = [
    r'(?i)(?:located in|location|based in|remote from|headquartered in)\s+([\w\s,]+)',
    r'(?i)(?:worked in|working in|relocated to)\s+([\w\s,]+)',
    r'(?i)(?:University of|College in)\s+([\w\s,]+)'
]