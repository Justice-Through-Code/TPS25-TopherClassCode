# enterprise_integration.py
# Most advanced example - Enterprise-level integration of all previous concepts

import json
import datetime
import random
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod

# Advanced integration patterns building on ALL previous files

class ConfigurationManager:
    """Manages system configuration - integrates module concepts from module_integration.py"""
    
    def __init__(self):
        self.config = {
            "system_name": "Educational Management System",
            "version": "2.0.0",
            "database_settings": {
                "host": "localhost",
                "port": 5432,
                "name": "school_db"
            },
            "notification_settings": {
                "email_enabled": True,
                "sms_enabled": False,
                "push_enabled": True
            },
            "grade_scale": {
                "A": 90, "B": 80, "C": 70, "D": 60, "F": 0
            }
        }
    
    def get_setting(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'database_settings.host')"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def update_setting(self, key_path: str, new_value: Any):
        """Update configuration value"""
        keys = key_path.split('.')
        config_section = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config_section:
                config_section[key] = {}
            config_section = config_section[key]
        
        # Set the final value
        config_section[keys[-1]] = new_value

class DataValidator:
    """Advanced data validation - extends basic_functions.py concepts"""
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Validate email address format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        
        return {
            "is_valid": is_valid,
            "email": email.lower() if is_valid else email,
            "error": None if is_valid else "Invalid email format"
        }
    
    @staticmethod
    def validate_student_data(data: Dict) -> Dict[str, Any]:
        """Comprehensive student data validation"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['first_name', 'last_name', 'student_id', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate email if present
        if 'email' in data and data['email']:
            email_result = DataValidator.validate_email(data['email'])
            if not email_result['is_valid']:
                errors.append(f"Invalid email: {email_result['error']}")
        
        # Validate student ID format (should be numeric and reasonable length)
        if 'student_id' in data:
            try:
                student_id = int(data['student_id'])
                if student_id <= 0 or student_id > 999999:
                    warnings.append("Student ID should be between 1 and 999999")
            except (ValueError, TypeError):
                errors.append("Student ID must be a valid number")
        
        # Validate names (should contain only letters and basic punctuation)
        for name_field in ['first_name', 'last_name']:
            if name_field in data and data[name_field]:
                name = data[name_field]
                if not name.replace(' ', '').replace('-', '').replace("'", '').isalpha():
                    warnings.append(f"{name_field} contains unusual characters")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validated_data": data
        }

class NotificationService:
    """Advanced notification system - integrates multiple communication channels"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.notification_log = []
    
    def send_notification(self, recipient: str, subject: str, message: str, 
                         notification_type: str = "email") -> Dict[str, Any]:
        """Send notification through specified channel"""
        
        # Check if notification type is enabled
        setting_key = f"notification_settings.{notification_type}_enabled"
        if not self.config.get_setting(setting_key, False):
            return {
                "success": False,
                "error": f"{notification_type.title()} notifications are disabled"
            }
        
        # Simulate sending notification
        notification_id = random.randint(10000, 99999)
        timestamp = datetime.datetime.now().isoformat()
        
        notification_record = {
            "id": notification_id,
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "type": notification_type,
            "timestamp": timestamp,
            "status": "sent"
        }
        
        self.notification_log.append(notification_record)
        
        return {
            "success": True,
            "notification_id": notification_id,
            "message": f"{notification_type.title()} sent successfully to {recipient}"
        }
    
    def get_notification_history(self, recipient: Optional[str] = None) -> List[Dict]:
        """Get notification history, optionally filtered by recipient"""
        if recipient:
            return [n for n in self.notification_log if n['recipient'] == recipient]
        return self.notification_log.copy()

class ReportGenerator:
    """Advanced reporting system - integrates all data processing capabilities"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.templates = {
            "student_progress": "Student Progress Report Template",
            "class_summary": "Class Summary Report Template", 
            "system_analytics": "System Analytics Report Template"
        }
    
    def generate_executive_summary(self, school_data: Dict) -> str:
        """Generate executive-level summary report"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_name = self.config.get_setting("system_name", "Unknown System")
        version = self.config.get_setting("version", "Unknown Version")
        
        # Extract metrics from school data
        total_students = len(school_data.get('students', []))
        total_classes = len(school_data.get('classes', []))
        total_teachers = len(school_data.get('teachers', []))
        
        # Calculate performance metrics
        all_grades = []
        for class_info in school_data.get('classes', []):
            for student_grade in class_info.get('student_grades', []):
                all_grades.append(student_grade.get('average', 0))
        
        avg_performance = sum(all_grades) / len(all_grades) if all_grades else 0
        
        report_sections = [
            "=" * 80,
            f"EXECUTIVE SUMMARY REPORT",
            f"System: {system_name} v{version}",
            f"Generated: {timestamp}",
            "=" * 80,
            "",
            "KEY METRICS:",
            f"• Total Students Enrolled: {total_students:,}",
            f"• Total Classes: {total_classes:,}",
            f"• Total Teachers: {total_teachers:,}",
            f"• Average Student Performance: {avg_performance:.1f}%",
            "",
            "SYSTEM HEALTH:",
            f"• Database Status: {'Connected' if total_students > 0 else 'No Data'}",
            f"• Email Notifications: {'Enabled' if self.config.get_setting('notification_settings.email_enabled') else 'Disabled'}",
            f"• System Uptime: 99.9%",  # Simulated
            "",
            "PERFORMANCE INSIGHTS:",
        ]
        
        # Add performance insights
        if all_grades:
            high_performers = len([g for g in all_grades if g >= 90])
            struggling_students = len([g for g in all_grades if g < 70])
            
            report_sections.extend([
                f"• High Performers (90%+): {high_performers} students ({(high_performers/len(all_grades)*100):.1f}%)",
                f"• Students Needing Support (<70%): {struggling_students} students ({(struggling_students/len(all_grades)*100):.1f}%)",
                f"• Class Average Distribution: {min(all_grades):.1f}% - {max(all_grades):.1f}%",
            ])
        
        report_sections.extend([
            "",
            "RECOMMENDATIONS:",
            "• Continue monitoring student performance trends",
            "• Consider additional support for struggling students", 
            "• Maintain current teaching strategies for high performers",
            "",
            "=" * 80,
            f"Report generated by {system_name}",
            "=" * 80
        ])
        
        return "\n".join(report_sections)

class EnterpriseEducationSystem:
    """Master integration class combining ALL previous concepts and patterns"""
    
    def __init__(self):
        # Initialize all integrated components
        self.config = ConfigurationManager()
        self.validator = DataValidator()
        self.notifications = NotificationService(self.config)
        self.reporter = ReportGenerator(self.config)
        
        # System data storage
        self.students = {}
        self.teachers = {}
        self.classes = {}
        self.system_logs = []
        
        # Initialize system
        self._log_system_event("System initialized", "INFO")
    
    def _log_system_event(self, message: str, level: str = "INFO"):
        """Internal method to log system events"""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "level": level,
            "message": message,
            "system": self.config.get_setting("system_name", "EES")
        }
        self.system_logs.append(log_entry)
        if level in ["ERROR", "CRITICAL"]:
            print(f"[{level}] {message}")
    
    def register_student(self, student_data: Dict) -> Dict[str, Any]:
        """Register a new student with full validation and notification"""
        # Step 1: Validate student data
        validation_result = self.validator.validate_student_data(student_data)
        
        if not validation_result["is_valid"]:
            self._log_system_event(f"Student registration failed: {validation_result['errors']}", "ERROR")
            return {
                "success": False,
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"]
            }
        
        # Step 2: Check for duplicate student ID
        student_id = int(student_data["student_id"])
        if student_id in self.students:
            error_msg = f"Student ID {student_id} already exists"
            self._log_system_event(error_msg, "ERROR")
            return {"success": False, "errors": [error_msg]}
        
        # Step 3: Create student record with enhanced data
        student_record = {
            "student_id": student_id,
            "first_name": student_data["first_name"].title(),
            "last_name": student_data["last_name"].title(),
            "email": student_data["email"].lower(),
            "registration_date": datetime.datetime.now().isoformat(),
            "status": "active",
            "classes_enrolled": [],
            "grades": {},
            "attendance_record": []
        }
        
        # Add optional fields
        optional_fields = ["phone", "address", "parent_email", "grade_level"]
        for field in optional_fields:
            if field in student_data and student_data[field]:
                student_record[field] = student_data[field]
        
        # Step 4: Store student record
        self.students[student_id] = student_record
        
        # Step 5: Send welcome notification
        welcome_subject = f"Welcome to {self.config.get_setting('system_name')}"
        welcome_message = f"""
Dear {student_record['first_name']} {student_record['last_name']},

Welcome to our educational system! Your student ID is {student_id}.

Please keep this information safe as you'll need it to access your account.

Best regards,
Academic Administration
        """.strip()
        
        notification_result = self.notifications.send_notification(
            student_record["email"], 
            welcome_subject, 
            welcome_message
        )
        
        # Step 6: Log successful registration
        self._log_system_event(f"Student registered: {student_record['first_name']} {student_record['last_name']} (ID: {student_id})", "INFO")
        
        return {
            "success": True,
            "student_id": student_id,
            "message": f"Student {student_record['first_name']} {student_record['last_name']} registered successfully",
            "warnings": validation_result["warnings"],
            "notification_sent": notification_result["success"]
        }
    
    def create_class(self, class_data: Dict) -> Dict[str, Any]:
        """Create a new class with teacher assignment"""
        required_fields = ["class_name", "teacher_id", "subject", "max_students"]
        
        # Validate required fields
        for field in required_fields:
            if field not in class_data or not class_data[field]:
                return {"success": False, "error": f"Missing required field: {field}"}
        
        class_id = f"{class_data['subject']}_{random.randint(1000, 9999)}"
        
        class_record = {
            "class_id": class_id,
            "class_name": class_data["class_name"],
            "subject": class_data["subject"],
            "teacher_id": class_data["teacher_id"],
            "max_students": int(class_data["max_students"]),
            "enrolled_students": [],
            "schedule": class_data.get("schedule", "TBD"),
            "created_date": datetime.datetime.now().isoformat(),
            "status": "active"
        }
        
        self.classes[class_id] = class_record
        self._log_system_event(f"Class created: {class_data['class_name']} (ID: {class_id})", "INFO")
        
        return {
            "success": True,
            "class_id": class_id,
            "message": f"Class '{class_data['class_name']}' created successfully"
        }
    
    def enroll_student_in_class(self, student_id: int, class_id: str) -> Dict[str, Any]:
        """Enroll student in class with capacity checking"""
        # Validate student exists
        if student_id not in self.students:
            return {"success": False, "error": f"Student ID {student_id} not found"}
        
        # Validate class exists
        if class_id not in self.classes:
            return {"success": False, "error": f"Class ID {class_id} not found"}
        
        class_info = self.classes[class_id]
        student_info = self.students[student_id]
        
        # Check if student already enrolled
        if student_id in class_info["enrolled_students"]:
            return {"success": False, "error": "Student already enrolled in this class"}
        
        # Check class capacity
        if len(class_info["enrolled_students"]) >= class_info["max_students"]:
            return {"success": False, "error": "Class is at maximum capacity"}
        
        # Enroll student
        class_info["enrolled_students"].append(student_id)
        student_info["classes_enrolled"].append(class_id)
        
        # Send enrollment notification
        enrollment_subject = f"Enrolled in {class_info['class_name']}"
        enrollment_message = f"""
Dear {student_info['first_name']},

You have been successfully enrolled in:
Class: {class_info['class_name']}
Subject: {class_info['subject']}
Schedule: {class_info['schedule']}

Please check your schedule and be prepared for the first class.

Best regards,
Academic Administration
        """.strip()
        
        self.notifications.send_notification(
            student_info["email"],
            enrollment_subject,
            enrollment_message
        )
        
        self._log_system_event(f"Student {student_id} enrolled in class {class_id}", "INFO")
        
        return {
            "success": True,
            "message": f"Student enrolled in {class_info['class_name']} successfully"
        }
    
    def generate_comprehensive_report(self) -> str:
        """Generate enterprise-level comprehensive system report"""
        # Prepare school data for reporting
        school_data = {
            "students": list(self.students.values()),
            "teachers": list(self.teachers.values()),
            "classes": []
        }
        
        # Enhance class data with student performance
        for class_id, class_info in self.classes.items():
            enhanced_class = class_info.copy()
            enhanced_class["student_grades"] = []
            
            # Simulate grades for enrolled students
            for student_id in class_info["enrolled_students"]:
                if student_id in self.students:
                    # Generate realistic grade distribution
                    base_grade = random.uniform(65, 95)
                    enhanced_class["student_grades"].append({
                        "student_id": student_id,
                        "average": round(base_grade, 1)
                    })
            
            school_data["classes"].append(enhanced_class)
        
        return self.reporter.generate_executive_summary(school_data)
    
    def run_system_diagnostics(self) -> Dict[str, Any]:
        """Run comprehensive system diagnostics"""
        diagnostics = {
            "system_status": "OPERATIONAL",
            "timestamp": datetime.datetime.now().isoformat(),
            "components": {},
            "statistics": {},
            "recommendations": []
        }
        
        # Check component health
        diagnostics["components"]["configuration"] = {
            "status": "OK",
            "settings_loaded": len(self.config.config) > 0
        }
        
        diagnostics["components"]["notifications"] = {
            "status": "OK",
            "total_sent": len(self.notifications.notification_log),
            "email_enabled": self.config.get_setting("notification_settings.email_enabled")
        }
        
        diagnostics["components"]["data_validation"] = {
            "status": "OK",
            "validator_available": self.validator is not None
        }
        
        # System statistics
        diagnostics["statistics"] = {
            "total_students": len(self.students),
            "total_classes": len(self.classes),
            "total_enrollments": sum(len(c["enrolled_students"]) for c in self.classes.values()),
            "system_logs": len(self.system_logs),
            "notifications_sent": len(self.notifications.notification_log)
        }
        
        # Generate recommendations
        if len(self.students) == 0:
            diagnostics["recommendations"].append("Consider adding student data to test system functionality")
        
        if len(self.classes) == 0:
            diagnostics["recommendations"].append("Create classes to enable full system functionality")
        
        avg_class_size = (diagnostics["statistics"]["total_enrollments"] / 
                         max(len(self.classes), 1))
        if avg_class_size < 5:
            diagnostics["recommendations"].append("Consider promoting enrollment to increase class sizes")
        
        return diagnostics

# Comprehensive demonstration of enterprise-level integration
if __name__ == "__main__":
    print("🎓 ENTERPRISE EDUCATION SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("This system integrates ALL concepts from previous files:")
    print("• Function integration (basic_functions.py)")
    print("• Class integration (simple_classes.py)")
    print("• Module integration (module_integration.py)")
    print("• Advanced system design (advanced_system.py)")
    print("=" * 60)
    
    # Initialize the enterprise system
    edu_system = EnterpriseEducationSystem()
    print(f"\n✅ System initialized: {edu_system.config.get_setting('system_name')}")
    
    # Demonstrate student registration with validation
    print("\n📝 STUDENT REGISTRATION DEMO:")
    print("-" * 40)
    
    sample_students = [
        {
            "student_id": "12001",
            "first_name": "alice",
            "last_name": "JOHNSON",
            "email": "alice.johnson@email.com",
            "grade_level": 10
        },
        {
            "student_id": "12002", 
            "first_name": "Bob",
            "last_name": "smith",
            "email": "bob.smith@email.com",
            "phone": "555-0123"
        },
        {
            "student_id": "invalid_id",  # This will cause validation error
            "first_name": "",
            "email": "invalid-email"
        }
    ]
    
    for i, student_data in enumerate(sample_students, 1):
        print(f"\nRegistering Student {i}:")
        result = edu_system.register_student(student_data)
        
        if result["success"]:
            print(f"  ✅ {result['message']}")
            if result.get("warnings"):
                print(f"  ⚠️  Warnings: {', '.join(result['warnings'])}")
        else:
            print(f"  ❌ Registration failed: {', '.join(result.get('errors', ['Unknown error']))}")
    
    # Demonstrate class creation
    print("\n🏫 CLASS CREATION DEMO:")
    print("-" * 40)
    
    sample_classes = [
        {
            "class_name": "Advanced Mathematics",
            "teacher_id": "T001",
            "subject": "Mathematics",
            "max_students": 25,
            "schedule": "MWF 9:00-10:00 AM"
        },
        {
            "class_name": "English Literature",
            "teacher_id": "T002", 
            "subject": "English",
            "max_students": 20,
            "schedule": "TTh 11:00-12:30 PM"
        }
    ]
    
    created_classes = []
    for class_data in sample_classes:
        result = edu_system.create_class(class_data)
        if result["success"]:
            print(f"✅ {result['message']}")
            created_classes.append(result["class_id"])
        else:
            print(f"❌ {result.get('error', 'Unknown error')}")
    
    # Demonstrate student enrollment
    print("\n📚 STUDENT ENROLLMENT DEMO:")
    print("-" * 40)
    
    # Enroll registered students in classes
    registered_students = [sid for sid in edu_system.students.keys()]
    
    for student_id in registered_students:
        for class_id in created_classes:
            result = edu_system.enroll_student_in_class(student_id, class_id)
            student_name = f"{edu_system.students[student_id]['first_name']} {edu_system.students[student_id]['last_name']}"
            class_name = edu_system.classes[class_id]['class_name']
            
            if result["success"]:
                print(f"✅ {student_name} enrolled in {class_name}")
            else:
                print(f"❌ Failed to enroll {student_name}: {result['error']}")
    
    # Run system diagnostics
    print("\n🔧 SYSTEM DIAGNOSTICS:")
    print("-" * 40)
    
    diagnostics = edu_system.run_system_diagnostics()
    print(f"Status: {diagnostics['system_status']}")
    print(f"Students: {diagnostics['statistics']['total_students']}")
    print(f"Classes: {diagnostics['statistics']['total_classes']}")
    print(f"Enrollments: {diagnostics['statistics']['total_enrollments']}")
    print(f"Notifications Sent: {diagnostics['statistics']['notifications_sent']}")
    
    if diagnostics["recommendations"]:
        print("\nRecommendations:")
        for rec in diagnostics["recommendations"]:
            print(f"  • {rec}")
    
    # Generate comprehensive report
    print("\n📊 COMPREHENSIVE SYSTEM REPORT:")
    print("-" * 40)
    
    report = edu_system.generate_comprehensive_report()
    print(report)
    
    print("\n🎉 DEMONSTRATION COMPLETE!")
    print("This enterprise system successfully integrates:")
    print("✓ Data validation and processing")
    print("✓ Configuration management") 
    print("✓ Notification services")
    print("✓ Advanced reporting")
    print("✓ Error handling and logging")
    print("✓ Multi-component architecture")