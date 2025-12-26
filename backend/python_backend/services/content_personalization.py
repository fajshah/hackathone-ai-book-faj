"""
Content personalization service for delivering experience-appropriate content
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from models.user import User


class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class HardwareKnowledgeLevel(Enum):
    NONE = "none"
    BASIC = "basic"
    ELECTRONICS = "electronics"
    ROBOTICS = "robotics"
    ADVANCED = "advanced"


@dataclass
class ContentLevel:
    beginner: str
    intermediate: str
    advanced: str


class ContentPersonalizationService:
    """
    Service for personalizing content based on user profile data
    """

    def __init__(self):
        # Content mapping based on experience level
        self.content_mapping = {
            "ai_fundamentals": ContentLevel(
                beginner="Introduction to AI concepts, basic machine learning algorithms, simple neural networks",
                intermediate="Deep learning fundamentals, CNNs and RNNs, training techniques, optimization",
                advanced="Advanced neural architectures, transformer models, research papers, cutting-edge techniques"
            ),
            "robotics_basics": ContentLevel(
                beginner="Introduction to robotics, basic kinematics, simple robot programming",
                intermediate="Robot control systems, sensor integration, path planning algorithms",
                advanced="Advanced robotics control, SLAM algorithms, humanoid robotics, real-time systems"
            ),
            "physical_ai": ContentLevel(
                beginner="Introduction to physical AI, basic concepts of embodied intelligence",
                intermediate="Physical AI principles, sensorimotor learning, robot learning techniques",
                advanced="Advanced physical AI research, embodied cognition, complex robot behaviors"
            ),
            "humanoid_robots": ContentLevel(
                beginner="Introduction to humanoid robots, basic design principles",
                intermediate="Humanoid locomotion, balance control, human-robot interaction",
                advanced="Advanced humanoid control, biologically-inspired robotics, complex behaviors"
            ),
            "reinforcement_learning": ContentLevel(
                beginner="Basic RL concepts, Q-learning, simple environments",
                intermediate="Deep RL, policy gradients, complex environments",
                advanced="Advanced RL research, multi-agent systems, sample efficient methods"
            ),
            "computer_vision": ContentLevel(
                beginner="Basic image processing, simple CNNs, object detection fundamentals",
                intermediate="Advanced CNNs, image segmentation, feature extraction",
                advanced="State-of-the-art vision models, 3D vision, vision-language models"
            ),
            "natural_language_processing": ContentLevel(
                beginner="Basic NLP, text processing, simple language models",
                intermediate="RNNs, attention mechanisms, transformer basics",
                advanced="Advanced transformers, large language models, specialized architectures"
            ),
            "sensor_integration": ContentLevel(
                beginner="Basic sensors, sensor reading, simple filtering",
                intermediate="Sensor fusion, advanced filtering, calibration techniques",
                advanced="Multi-sensor systems, real-time processing, sensor networks"
            )
        }

        # Interest-based content tags
        self.interest_content_mapping = {
            "AI": ["ai_fundamentals", "reinforcement_learning", "computer_vision", "natural_language_processing"],
            "Robotics": ["robotics_basics", "humanoid_robots", "reinforcement_learning", "sensor_integration"],
            "Web": ["web_development", "api_design", "frontend_for_ai"],
            "Mobile": ["mobile_robotics", "mobile_apps_for_robotics"],
            "Embedded": ["embedded_systems", "sensor_integration", "real_time_processing"],
            "Data": ["data_science", "machine_learning", "computer_vision", "ai_fundamentals"]
        }

    def get_personalized_content(self, user: User) -> Dict[str, Any]:
        """
        Get personalized content based on user profile
        """
        experience_level = user.software_experience or "beginner"
        hardware_knowledge = user.hardware_knowledge or "none"
        interests = user.interests or []

        # Determine content level based on experience
        content_level = self._get_content_for_experience_level(experience_level)

        # Get content based on hardware knowledge
        hardware_content = self._get_hardware_specific_content(hardware_knowledge)

        # Get content based on interests
        interest_content = self._get_interest_based_content(interests)

        # Combine all content
        all_content = self._combine_content(content_level, hardware_content, interest_content)

        # Generate learning path based on user profile
        learning_path = self._generate_learning_path(user)

        return {
            "user_profile": {
                "experience_level": experience_level,
                "hardware_knowledge": hardware_knowledge,
                "interests": interests
            },
            "personalized_content": all_content,
            "learning_path": learning_path,
            "difficulty_level": experience_level,
            "recommended_next_steps": self._get_next_steps(user)
        }

    def _get_content_for_experience_level(self, experience_level: str) -> Dict[str, str]:
        """
        Get content appropriate for the user's experience level
        """
        content = {}

        for topic, level_content in self.content_mapping.items():
            if experience_level == "advanced":
                content[topic] = level_content.advanced
            elif experience_level == "intermediate":
                content[topic] = level_content.intermediate
            else:  # beginner
                content[topic] = level_content.beginner

        return content

    def _get_hardware_specific_content(self, hardware_knowledge: str) -> List[str]:
        """
        Get hardware-specific content based on user's knowledge level
        """
        hardware_content = []

        if hardware_knowledge in ["electronics", "robotics", "advanced"]:
            hardware_content.extend([
                "Circuit design for AI applications",
                "Sensor selection and integration",
                "Motor control systems",
                "Real-time embedded systems"
            ])

        if hardware_knowledge in ["robotics", "advanced"]:
            hardware_content.extend([
                "Robot kinematics and dynamics",
                "Hardware-in-the-loop simulation",
                "Robot operating systems (ROS)"
            ])

        if hardware_knowledge == "advanced":
            hardware_content.extend([
                "Custom hardware for AI (TPUs, neuromorphic)",
                "High-performance computing for robotics",
                "Hardware security for AI systems"
            ])

        return hardware_content

    def _get_interest_based_content(self, interests: List[str]) -> Dict[str, List[str]]:
        """
        Get content based on user's interests
        """
        interest_content = {}

        for interest in interests:
            if interest in self.interest_content_mapping:
                topics = self.interest_content_mapping[interest]
                interest_content[interest] = []

                for topic in topics:
                    if topic in self.content_mapping:
                        # Get content appropriate for user's level
                        experience_level = "advanced" if "advanced" in self.content_mapping[topic].advanced.lower() else \
                                         "intermediate" if "intermediate" in self.content_mapping[topic].intermediate.lower() else "beginner"

                        if experience_level == "advanced":
                            interest_content[interest].append(self.content_mapping[topic].advanced)
                        elif experience_level == "intermediate":
                            interest_content[interest].append(self.content_mapping[topic].intermediate)
                        else:
                            interest_content[interest].append(self.content_mapping[topic].beginner)

        return interest_content

    def _combine_content(self, level_content: Dict[str, str],
                        hardware_content: List[str],
                        interest_content: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Combine different types of content
        """
        return {
            "by_level": level_content,
            "by_hardware": hardware_content,
            "by_interests": interest_content
        }

    def _generate_learning_path(self, user: User) -> List[Dict[str, str]]:
        """
        Generate a personalized learning path based on user profile
        """
        experience_level = user.software_experience or "beginner"
        hardware_knowledge = user.hardware_knowledge or "none"
        interests = user.interests or []

        learning_path = []

        # Base path for all users
        if experience_level == "beginner":
            learning_path.extend([
                {"topic": "AI Fundamentals", "level": "beginner", "duration": "2-3 weeks", "prerequisites": []},
                {"topic": "Programming Basics", "level": "beginner", "duration": "1-2 weeks", "prerequisites": []},
                {"topic": "Mathematics for AI", "level": "beginner", "duration": "3-4 weeks", "prerequisites": []}
            ])
        elif experience_level == "intermediate":
            learning_path.extend([
                {"topic": "Advanced AI Concepts", "level": "intermediate", "duration": "3-4 weeks", "prerequisites": ["AI Fundamentals"]},
                {"topic": "Machine Learning", "level": "intermediate", "duration": "4-5 weeks", "prerequisites": ["AI Fundamentals"]},
                {"topic": "Deep Learning", "level": "intermediate", "duration": "5-6 weeks", "prerequisites": ["Machine Learning"]}
            ])
        else:  # advanced
            learning_path.extend([
                {"topic": "Research Methods in AI", "level": "advanced", "duration": "4-6 weeks", "prerequisites": ["Deep Learning"]},
                {"topic": "Advanced Robotics", "level": "advanced", "duration": "6-8 weeks", "prerequisites": ["Machine Learning"]},
                {"topic": "Specialized Topics", "level": "advanced", "duration": "8-10 weeks", "prerequisites": ["Research Methods in AI"]}
            ])

        # Add hardware-specific path if applicable
        if hardware_knowledge in ["electronics", "robotics", "advanced"]:
            if experience_level == "beginner":
                learning_path.insert(1, {"topic": "Basic Electronics", "level": "beginner", "duration": "2-3 weeks", "prerequisites": []})
            elif experience_level == "intermediate":
                learning_path.insert(2, {"topic": "Robotics Hardware", "level": "intermediate", "duration": "3-4 weeks", "prerequisites": ["Basic Electronics"]})
            else:
                learning_path.insert(2, {"topic": "Advanced Hardware Systems", "level": "advanced", "duration": "4-5 weeks", "prerequisites": ["Robotics Hardware"]})

        # Add interest-specific content
        for interest in interests:
            if interest == "AI":
                if experience_level == "beginner":
                    learning_path.append({"topic": "AI Applications", "level": "beginner", "duration": "2-3 weeks", "prerequisites": ["AI Fundamentals"]})
                elif experience_level == "intermediate":
                    learning_path.append({"topic": "Advanced AI Applications", "level": "intermediate", "duration": "3-4 weeks", "prerequisites": ["Advanced AI Concepts"]})
                else:
                    learning_path.append({"topic": "AI Research Frontiers", "level": "advanced", "duration": "4-5 weeks", "prerequisites": ["Research Methods in AI"]})

            elif interest == "Robotics":
                if experience_level == "beginner":
                    learning_path.append({"topic": "Introduction to Robotics", "level": "beginner", "duration": "3-4 weeks", "prerequisites": ["AI Fundamentals"]})
                elif experience_level == "intermediate":
                    learning_path.append({"topic": "Robotics Programming", "level": "intermediate", "duration": "4-5 weeks", "prerequisites": ["Machine Learning", "Robotics Hardware"]})
                else:
                    learning_path.append({"topic": "Humanoid Robotics Research", "level": "advanced", "duration": "6-8 weeks", "prerequisites": ["Advanced Robotics"]})

        return learning_path

    def _get_next_steps(self, user: User) -> List[str]:
        """
        Get recommended next steps based on user profile
        """
        experience_level = user.software_experience or "beginner"
        hardware_knowledge = user.hardware_knowledge or "none"
        interests = user.interests or []

        next_steps = []

        # General next steps based on experience
        if experience_level == "beginner":
            next_steps.extend([
                "Complete the AI fundamentals course",
                "Practice basic programming exercises",
                "Explore introductory robotics concepts"
            ])
        elif experience_level == "intermediate":
            next_steps.extend([
                "Dive deeper into machine learning algorithms",
                "Work on practical AI projects",
                "Explore specialized areas of interest"
            ])
        else:  # advanced
            next_steps.extend([
                "Read current research papers",
                "Contribute to open source AI projects",
                "Explore cutting-edge applications"
            ])

        # Hardware-specific next steps
        if hardware_knowledge in ["electronics", "robotics", "advanced"]:
            if experience_level == "beginner":
                next_steps.insert(0, "Learn basic electronics principles")
            elif experience_level == "intermediate":
                next_steps.insert(0, "Build a simple robot project")
            else:
                next_steps.insert(0, "Design custom hardware for AI applications")

        # Interest-specific next steps
        if "AI" in interests:
            next_steps.append("Explore AI ethics and responsible AI practices")

        if "Robotics" in interests:
            next_steps.append("Join a robotics competition or community")

        if "Data" in interests:
            next_steps.append("Work on data analysis projects with AI")

        return next_steps[:5]  # Return top 5 recommendations