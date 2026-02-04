import json

with open('datas.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

target_roles = loaded_data["target_roles"]


# PROJECTS SEEDING
# title= "💊 DrugVerify – Global Pharmaceutical Traceability & Authentication System"
# technologies= ["Python", "Django", "OpenCV", "NumPy", "SQL/SQLite", "HTML5", "Bootstrap 5", "CSS3", "JavaScript (html5-qrcode)", "Git", "UV"]
# github_url= "https://github.com/aramydcd/Drug-Verification-System"
# live_demo_url= "https://myapp.com"
# image_file= "default.jpg"

# description = """
# 💊 DrugVerify is a high-integrity web ecosystem engineered to eliminate pharmaceutical counterfeiting and supply chain fraud. By bridging the gap between manufacturers and the end consumer, the platform provides a "Single Source of Truth" for medication authenticity. The system is architected to handle complex data relationships while offering a seamless, mobile-first experience for field verification.

# KEY ENGINEERING CONTRIBUTIONS:
# 1. Full-Stack CRUD Architecture (Manufacturer Suite):
# Designed and implemented a secure, role-based management dashboard for verified pharmaceutical manufacturers:
#     • Inventory Control: Enables manufacturers to perform full CRUD (Create, Read, Update, Delete) operations on drug profiles, batch records, and unique identifiers.
#     • Data Governance: Implemented strict ownership logic to ensure manufacturers can only modify their own authorized datasets, utilizing Django’s robust ORM and middleware.

# 2. Hybrid Computer Vision Verification Pipeline:
# To ensure 100% availability across all devices, I engineered a dual-channel scanning solution:
#     • Frontend (Real-Time): Integrated a JavaScript-based camera scanner Implementing the 'html5-qrcode' library with custom event-handling for automated form submission and for instantaneous, client-side authentication.
#     • Backend (High-Performance): Developed a fail-safe Python pipeline. When users upload images, the backend reads the `InMemoryUploadedFile` as a raw byte stream into a NumPy buffer, processing it via OpenCV (`cv2`) for server-side decoding. This eliminates disk I/O bottlenecks and optimizes RAM usage.

# 3. Security & Integrity Protocols:
#     • Audit Logging: Engineered a persistent audit trail in an immutable log, recording user metadata, timestamps, and validation results to help regulatory bodies identify hotspots of counterfeit activity.
#     • Session Management: Implemented multi-level authentication and secure session handling to protect sensitive manufacturer data and administrative controls.
#     • Scalable Schema: Architected a relational database schema that handles complex "One-to-Many" relationships between Manufacturers and their respective Drug Batches.

# CORE FUNCTIONALITY
# Features & Implementation:
# 1. Manufacturer Dashboard: Secure CRUD operations for drug and batch management.
# 2. Real-time Authentication: Live camera-based QR scanning with auto-submit logic.
# 3. Server-side Processing: OpenCV-powered image decoding for uploaded pack photos.
# 4. Traceability: Unique batch-to-manufacturer linking and verification history.

# THE IMPACT
# The result is a production-ready platform that solves a real-world problem. It demonstrates my ability to handle binary data processing, asynchronous frontend events, and secure backend architecture within a single, unified product.
# """
# newProject = {
#     "title": title,
#     "description": description,
#     "technologies": technologies,
#     "github_url": github_url,
#     "live_demo_url": live_demo_url,
#     "image_file": image_file
# }



# ROLE SEEDING
# "cv_filename":"backend_developer_Abdulazeez_Abdulakeem_Backend_Developer_CV.pdf"

newRole = {
    "title": "Full-Stack Engineer",
    "icon_class": "bi-window-stack",
    "description": "Bridging the gap between backends and frontends..."
}
counter = 1




for role in target_roles:
    # if "ColorSync" in pro["title"]:
    #     pro["description"] = okay
        
    print(f"PROJECTS {counter}\n{role["title"]}\n{role["description"]}\n\n")
    counter +=1
    

loaded_data["target_roles"] = target_roles

# loaded_data = {"metadata": loaded_data}
with open('datas.json', 'w') as file:
    json.dump(loaded_data, file, indent=4)

# print("\n\n\n\n")
# print(loaded_data)
    

# print(projects)


