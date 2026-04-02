COURSES = [
    {
        "course_name": "Python for Everybody",
        "skills": "python programming basics coding",
        "description": "learn python from scratch with real examples",
        "link": "https://www.coursera.org/learn/python"
    },
    {
        "course_name": "Machine Learning by Andrew Ng",
        "skills": "machine learning ai data science algorithms",
        "description": "supervised and unsupervised learning techniques",
        "link": "https://www.coursera.org/learn/machine-learning"
    },
    {
        "course_name": "Data Science Specialization",
        "skills": "data science analysis statistics python",
        "description": "data analysis and visualization using python",
        "link": "https://www.coursera.org/specializations/jhu-data-science"
    },
    {
        "course_name": "Web Development Bootcamp",
        "skills": "html css javascript frontend backend web",
        "description": "build modern websites using html css js",
        "link": "https://www.coursera.org/learn/web-development"
    },
    {
        "course_name": "Deep Learning Specialization",
        "skills": "deep learning neural networks ai",
        "description": "neural networks and deep learning models",
        "link": "https://www.coursera.org/specializations/deep-learning"
    },
    {
        "course_name": "SQL for Data Science",
        "skills": "sql database querying data analysis",
        "description": "learn sql queries for data analysis",
        "link": "https://www.coursera.org/learn/sql-for-data-science"
    },
    {
        "course_name": "Java Programming",
        "skills": "java programming object oriented",
        "description": "learn java programming from basics",
        "link": "https://www.coursera.org/learn/java-programming"
    },
    {
        "course_name": "C++ Programming",
        "skills": "c++ programming data structures",
        "description": "learn c++ and problem solving",
        "link": "https://www.coursera.org/learn/cpp"
    },
    {
        "course_name": "Computer Vision Basics",
        "skills": "computer vision image processing ai",
        "description": "image recognition and processing techniques",
        "link": "https://www.coursera.org/learn/computer-vision"
    },
    {
        "course_name": "Natural Language Processing",
        "skills": "nlp text processing ai machine learning",
        "description": "text analysis and language models",
        "link": "https://www.coursera.org/learn/nlp"
    },
    {
        "course_name": "Project Management Principles",
        "skills": "project management leadership planning",
        "description": "manage projects efficiently",
        "link": "https://www.coursera.org/learn/project-management"
    },
    {
        "course_name": "Data Analysis with Excel",
        "skills": "excel data analysis visualization",
        "description": "analyze data using excel tools",
        "link": "https://www.coursera.org/learn/excel-data-analysis"
    },
    {
        "course_name": "Cloud Computing Basics",
        "skills": "cloud computing aws azure devops",
        "description": "introduction to cloud platforms",
        "link": "https://www.coursera.org/learn/cloud-computing"
    },
    {
        "course_name": "Big Data with Spark",
        "skills": "big data spark hadoop data processing",
        "description": "process large datasets using spark",
        "link": "https://www.coursera.org/learn/big-data"
    },
    {
        "course_name": "Cyber Security Fundamentals",
        "skills": "cyber security networking encryption",
        "description": "protect systems and networks",
        "link": "https://www.coursera.org/learn/cyber-security"
    }
]

courses = COURSES

# ------------------ SKILL → TOP COURSERA COURSE ------------------

skill_course_map = {

    # PROGRAMMING
    "python": {
        "course_name": "Python for Everybody Specialization",
        "link": "https://www.coursera.org/specializations/python"
    },
    "java": {
        "course_name": "Java Programming and Software Engineering Fundamentals",
        "link": "https://www.coursera.org/specializations/java-programming"
    },
    "c++": {
        "course_name": "C++ For C Programmers",
        "link": "https://www.coursera.org/learn/c-plus-plus-a"
    },

    # DATA SCIENCE
    "data science": {
        "course_name": "IBM Data Science Professional Certificate",
        "link": "https://www.coursera.org/professional-certificates/ibm-data-science"
    },
    "data analysis": {
        "course_name": "Google Data Analytics Professional Certificate",
        "link": "https://www.coursera.org/professional-certificates/google-data-analytics"
    },
    "statistics": {
        "course_name": "Statistics with Python Specialization",
        "link": "https://www.coursera.org/specializations/statistics-with-python"
    },

    # MACHINE LEARNING / AI
    "machine learning": {
        "course_name": "Machine Learning by Andrew Ng",
        "link": "https://www.coursera.org/learn/machine-learning"
    },
    "deep learning": {
        "course_name": "Deep Learning Specialization",
        "link": "https://www.coursera.org/specializations/deep-learning"
    },
    "nlp": {
        "course_name": "Natural Language Processing Specialization",
        "link": "https://www.coursera.org/specializations/natural-language-processing"
    },
    "computer vision": {
        "course_name": "Computer Vision Basics",
        "link": "https://www.coursera.org/learn/computer-vision-basics"
    },

    # DATABASE
    "sql": {
        "course_name": "SQL for Data Science",
        "link": "https://www.coursera.org/learn/sql-for-data-science"
    },
    "database": {
        "course_name": "Databases and SQL for Data Science",
        "link": "https://www.coursera.org/learn/sql-data-science"
    },

    # WEB DEVELOPMENT
    "html": {
        "course_name": "HTML, CSS, and JavaScript for Web Developers",
        "link": "https://www.coursera.org/learn/html-css-javascript-for-web-developers"
    },
    "css": {
        "course_name": "HTML, CSS, and JavaScript for Web Developers",
        "link": "https://www.coursera.org/learn/html-css-javascript-for-web-developers"
    },
    "javascript": {
        "course_name": "Programming with JavaScript",
        "link": "https://www.coursera.org/learn/programming-with-javascript"
    },
    "react": {
        "course_name": "Front-End Web Development with React",
        "link": "https://www.coursera.org/learn/front-end-react"
    },
    "node": {
        "course_name": "Server-side Development with NodeJS",
        "link": "https://www.coursera.org/learn/server-side-nodejs"
    },

    # BIG DATA
    "big data": {
        "course_name": "Big Data Specialization",
        "link": "https://www.coursera.org/specializations/big-data"
    },
    "spark": {
        "course_name": "Big Data Analysis with Scala and Spark",
        "link": "https://www.coursera.org/learn/scala-spark-big-data"
    },

    # CLOUD
    "cloud computing": {
        "course_name": "Cloud Computing Specialization",
        "link": "https://www.coursera.org/specializations/cloud-computing"
    },
    "aws": {
        "course_name": "AWS Fundamentals Specialization",
        "link": "https://www.coursera.org/specializations/aws-fundamentals"
    },

    # DEVOPS
    "devops": {
        "course_name": "DevOps on AWS Specialization",
        "link": "https://www.coursera.org/specializations/aws-devops"
    },
    "docker": {
        "course_name": "Introduction to Containers w/ Docker, Kubernetes & OpenShift",
        "link": "https://www.coursera.org/learn/containers-docker-kubernetes-openshift"
    },

    # CYBER SECURITY
    "cyber security": {
        "course_name": "IBM Cybersecurity Analyst",
        "link": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst"
    },
    "ethical hacking": {
        "course_name": "Introduction to Cyber Security",
        "link": "https://www.coursera.org/learn/intro-cyber-security"
    },

    # ARTIFICIAL INTELLIGENCE
    "artificial intelligence": {
        "course_name": "AI for Everyone",
        "link": "https://www.coursera.org/learn/ai-for-everyone"
    },

    # PROJECT MANAGEMENT
    "project management": {
        "course_name": "Google Project Management",
        "link": "https://www.coursera.org/professional-certificates/google-project-management"
    }
}