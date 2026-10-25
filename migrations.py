"""
One-time Migration & Indexing for MongoDB.
All video details are stored and managed directly in MongoDB.
"""

from datetime import datetime, timezone

from pymongo import UpdateOne


SIMPLIFIED_VIDEO_TITLES = {
    "4NzqT_at4fc": "Operating Systems - Important Questions",
    "7zEvvM4Dueg": "Operating Systems - Complete Revision",
    "NCD68uZZCsQ": "Operating Systems - Unit 5",
    "pnK5UyAdG1k": "Operating Systems - Unit 4",
    "hxOA_u8y_0U": "Operating Systems - Unit 3",
    "sYm12jNPCao": "Operating Systems - Unit 2",
    "Kq0zz8fHXRc": "Operating Systems - Unit 1",
    "CMLyUh1xPdY": "COA - Important Questions",
    "h9aHz0PUzTg": "COA - Complete Revision",
    "izqkUj0JLd0": "COA - Unit 5",
    "kzvrNNqepAk": "COA - Unit 4",
    "vp8geYIKmlw": "COA - Unit 3",
    "2t4AQs7SjAY": "COA - Unit 2",
    "cnEnXjeZO8U": "COA - Unit 1",
    "UxTklWTfNEI": "Software Engineering - Complete Revision",
    "2LA3s5j_SX0": "Software Engineering - Unit 5",
    "3c0xCe-wt84": "Software Engineering - Unit 4",
    "tXYbYiw8NVM": "Software Engineering - Unit 3",
    "QugOsveKh5A": "Software Engineering - Unit 2",
    "wG7sfHLWtjI": "Software Engineering - Unit 1",
    "v8pxSieXMlM": "DBMS - Unit 1",
}

MIGRATED_VIDEOS = [{'created_at': '2026-10-18T11:16:53.221543+00:00',
  'description': '🚨 Operating System Exam Near? This is your Last Moment Revision!\n'
                 '\n'
                 'PDF LINK - https://drive.google.com/file/d/1RA-CtZHT8BqXmfJL6xe45QEDBV4ZIdpN/view?usp=sharing\n'
                 '\n'
                 'Preparing for RGPV B.Tech 4th Semester Operating System (CS-405)? This long-form revision video '
                 'focuses on the most important and high-priority topics from all 5 units, so you can revise the key '
                 'concepts before your exam without wasting time.\n'
                 '\n'
                 '🔥 UNIT 1 — OPERATING SYSTEM\n'
                 '\n'
                 'OS Definition, Goals, Functions & Types\n'
                 'Operating System Services\n'
                 'System Calls\n'
                 'Buffering & Spooling\n'
                 '\n'
                 '🔥 UNIT 2 — FILE SYSTEMS\n'
                 '\n'
                 'File Concepts & Operations\n'
                 'File Allocation Methods\n'
                 'Directory Structures\n'
                 'Disk Scheduling — SSTF, SCAN & LOOK\n'
                 'Disk Scheduling Numericals\n'
                 'File Protection\n'
                 '\n'
                 '🔥 UNIT 3 — PROCESS & MEMORY MANAGEMENT\n'
                 '\n'
                 'Process States\n'
                 'CPU Scheduling Algorithms\n'
                 'Gantt Chart Numericals\n'
                 'Threads & Process vs Thread\n'
                 'Paging & Segmentation\n'
                 'Virtual Memory & Demand Paging\n'
                 'Page Replacement Algorithms\n'
                 'Thrashing\n'
                 '\n'
                 '🔥 UNIT 4 — SYNCHRONIZATION & DEADLOCKS\n'
                 '\n'
                 'Critical Section Problem\n'
                 'Process Synchronization\n'
                 'Semaphores\n'
                 'Dining Philosophers\n'
                 'Deadlock\n'
                 'Deadlock Prevention & Avoidance\n'
                 'Banker’s Algorithm\n'
                 'Deadlock Recovery\n'
                 '\n'
                 '🔥 UNIT 5 — DISTRIBUTED & NETWORK OS\n'
                 '\n'
                 'Network Operating System\n'
                 'Distributed Operating System\n'
                 'Design Issues & Network Transparency\n'
                 'Distributed File System\n'
                 'RPC\n'
                 'Process Migration\n'
                 'Multiprocessor OS\n'
                 'UNIX/Linux & Kernel Architecture\n'
                 '🧮 MUST-REVISE NUMERICALS\n'
                 '\n'
                 'CPU Scheduling • Disk Scheduling • Page Replacement • Banker’s Algorithm • Segmentation Address '
                 'Translation\n'
                 '\n'
                 '🎯 This video is especially useful for:\n'
                 '✅ Last-minute exam revision\n'
                 '✅ One-night-before-exam preparation\n'
                 '✅ RGPV CS-405\n'
                 '✅ B.Tech 4th Semester\n'
                 '✅ Important topics revision\n'
                 '✅ PYQ-oriented preparation\n'
                 '✅ Quick full-syllabus revision\n'
                 '\n'
                 "⚡ Don't try to study everything at the last moment. Focus on the topics that matter most.\n"
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and exam-focused revision.\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSRevision #LastMinuteRevision #OSImportantTopics '
                 '#OSExamPreparation #RGPVExam #BTech #BTech4thSem #RGPVPYQ #OperatingSystemRGPV #ComputerScience #CSE '
                 '#ExamPreparation\n'
                 '\n'
                 'Tags \n'
                 '\n'
                 'OS Last Moment Revision, Operating System Last Minute Revision, OS Important Topics, OS Revision, OS '
                 'One Shot, CS405, RGPV CS405, RGPV Operating System, RGPV OS, OS Exam Preparation, RGPV Exam, OS PYQ, '
                 'RGPV PYQ, BTech 4th Sem, OS Unit 1, OS Unit 2, OS Unit 3, OS Unit 4, OS Unit 5, CPU Scheduling, '
                 'Paging, Deadlock, Banker’s Algorithm, File Systems, OS Numericals, TSUKOMI PADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1RA-CtZHT8BqXmfJL6xe45QEDBV4ZIdpN/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'os-last-moment-revision-most-important-topics-numericals-rgpv-cs-405-btech-4th-sem',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'OS Last Moment Revision 🔥 | Most Important Topics & Numericals | RGPV CS-405 | B.Tech 4th Sem',
  'unit': 'Important Questions',
  'updated_at': '2026-10-18T11:16:53.221558+00:00',
  'year': '2nd Year',
  'youtube_id': '4NzqT_at4fc',
  'youtube_url': 'https://www.youtube.com/watch?v=4NzqT_at4fc'},
 {'created_at': '2026-10-18T11:16:53.221575+00:00',
  'description': '📘 Operating System (CS-405) — All 5 Units Complete One-Shot\n'
                 '\n'
                 'PDF LINK - https://drive.google.com/file/d/1RA-CtZHT8BqXmfJL6xe45QEDBV4ZIdpN/view?usp=sharing\n'
                 '\n'
                 'Preparing for your RGPV B.Tech 4th Semester Operating System exam? This complete One-Shot covers the '
                 'important topics from all 5 units in one video, making it perfect for quick revision and exam '
                 'preparation. 🚀\n'
                 '\n'
                 '🔥 ALL 5 UNITS COVERED\n'
                 '\n'
                 '🔴 UNIT 1 — Operating System\n'
                 '• OS Definition, Goals, Functions & Types\n'
                 '• Evolution of Operating Systems\n'
                 '• OS Characteristics & Features\n'
                 '• Operating System Services\n'
                 '• System Calls\n'
                 '• Utility Programs\n'
                 '• Buffering & Spooling\n'
                 '\n'
                 '🟡 UNIT 2 — File Systems\n'
                 '• File Concept, Attributes & Operations\n'
                 '• File Allocation Methods\n'
                 '• Directory Structures\n'
                 '• Disk Organization\n'
                 '• Disk Scheduling — SSTF, SCAN & LOOK\n'
                 '• Disk Scheduling Numericals\n'
                 '• File Protection\n'
                 '• File System Modules & System Calls\n'
                 '• Tape Organization\n'
                 '\n'
                 '🟢 UNIT 3 — Process & Memory Management\n'
                 '• Process States & Schedulers\n'
                 '• CPU Scheduling Algorithms\n'
                 '• Gantt Chart Numericals\n'
                 '• Threads & Process vs Thread\n'
                 '• Paging & Segmentation\n'
                 '• Virtual Memory & Demand Paging\n'
                 '• Page Replacement Algorithms\n'
                 '• Thrashing\n'
                 '• Dynamic Loading & Linking\n'
                 '• Paged Segmentation\n'
                 '• Multiprocessor Scheduling\n'
                 '\n'
                 '🟣 UNIT 4 — Synchronization & Deadlocks\n'
                 '• Concurrency\n'
                 '• Mutual Exclusion & Critical Section\n'
                 '• Process Synchronization & IPC\n'
                 '• Semaphores\n'
                 '• WAIT & SIGNAL Operations\n'
                 '• Dining Philosophers Problem\n'
                 '• Deadlock & Characterization\n'
                 '• Deadlock Prevention & Avoidance\n'
                 '• Banker’s Algorithm 🧮\n'
                 '• Deadlock Recovery\n'
                 '• I/O Operations\n'
                 '\n'
                 '🟠 UNIT 5 — Distributed & Network Operating Systems\n'
                 '• Network Operating System\n'
                 '• Distributed Operating System & Design Issues\n'
                 '• Network Transparency\n'
                 '• Failures in Distributed Systems\n'
                 '• Distributed File System\n'
                 '• Remote Procedure Call (RPC)\n'
                 '• Process Migration\n'
                 '• Multiprocessor Operating System\n'
                 '• UNIX/Linux & Kernel Architecture\n'
                 '• UNIX/Linux & Windows Case Study\n'
                 '\n'
                 '🎯 Perfect for:\n'
                 '✅ RGPV CS-405 Exam Preparation\n'
                 '✅ B.Tech 4th Semester Revision\n'
                 '✅ Complete OS Syllabus Revision\n'
                 '✅ Important Topics Revision\n'
                 '✅ PYQ-Oriented Preparation\n'
                 '✅ Last-Minute Exam Preparation\n'
                 '✅ One-Shot Full Revision\n'
                 '\n'
                 '🧮 Important Numericals:\n'
                 'CPU Scheduling • Disk Scheduling • Page Replacement • Banker’s Algorithm • Segmentation Address '
                 'Translation\n'
                 '\n'
                 '🔥 All 5 Units. One Video. Complete Operating System Revision.\n'
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and exam-focused revision.\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSOneShot #OperatingSystemOneShot #OSRevision '
                 '#RGPVExam #BTech #BTech4thSem #RGPVPYQ #OSImportantTopics #OperatingSystemRGPV #ComputerScience #CSE '
                 '#ExamPreparation #LastMinuteRevision #OneShot',
  'notes_url': 'https://drive.google.com/file/d/1RA-CtZHT8BqXmfJL6xe45QEDBV4ZIdpN/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'operating-system-complete-one-shot-all-5-units-rgpv-cs-405-btech-4th-sem-full-revision',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'Operating System Complete One Shot 🔥 | All 5 Units | RGPV CS-405 | B.Tech 4th Sem | Full Revision',
  'unit': 'Complete Revision',
  'updated_at': '2026-10-18T11:16:53.221577+00:00',
  'year': '2nd Year',
  'youtube_id': '7zEvvM4Dueg',
  'youtube_url': 'https://www.youtube.com/watch?v=7zEvvM4Dueg'},
 {'created_at': '2026-10-18T11:16:53.221587+00:00',
  'description': '📘 Operating System Unit 5 — Complete One-Shot Revision | RGPV CS-405\n'
                 '\n'
                 'PDF LINK  - https://drive.google.com/file/d/1w2SQDx3OX9CDFNboNkN_S_5fbtqtTZxL/view?usp=sharing\n'
                 '\n'
                 'Preparing for your RGPV B.Tech 4th Semester Operating System exam? This video covers the important '
                 'Network Operating Systems, Distributed Operating Systems, Multiprocessor OS and UNIX/Linux concepts '
                 'from Unit 5 in one complete, exam-focused revision video. 🚀\n'
                 '\n'
                 '🔥 UNIT 5 — TOPICS COVERED:\n'
                 '\n'
                 'Network Operating System\n'
                 'Distributed Operating System & Design Issues\n'
                 'Network Transparency\n'
                 'Failures in Distributed Systems\n'
                 'Distributed File System\n'
                 'Remote Procedure Call (RPC)\n'
                 'Process Migration\n'
                 'Multiprocessor Operating System\n'
                 'UNIX/Linux Operating System & Kernel Architecture\n'
                 'Case Study: UNIX/Linux & Windows\n'
                 '\n'
                 '🎯 Perfect for:\n'
                 '• RGPV CS-405 Exam Preparation\n'
                 '• B.Tech 4th Semester OS Revision\n'
                 '• Unit 5 Complete Revision\n'
                 '• Distributed Operating Systems\n'
                 '• Network Operating Systems\n'
                 '• UNIX/Linux Kernel Architecture\n'
                 '• Last-Minute Exam Preparation\n'
                 '• PYQ-Oriented Study\n'
                 '\n'
                 '📚 Revise Unit 5 and strengthen the important concepts for your RGPV Operating System exam.\n'
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and complete unit-wise revision. 🔥\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSUnit5 #OSOneShot #OperatingSystemOneShot '
                 '#DistributedOperatingSystem #NetworkOperatingSystem #DistributedSystems #UNIX #Linux #Windows #BTech '
                 '#BTech4thSem #RGPVExam #OSRevision #ExamPreparation #RGPVPYQ #ComputerScience #CSE '
                 '#EngineeringStudents',
  'notes_url': 'https://drive.google.com/file/d/1w2SQDx3OX9CDFNboNkN_S_5fbtqtTZxL/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'os-unit-5-one-shot-distributed-network-os-rgpv-cs-405-btech-4th-sem',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'OS Unit 5 One Shot 🔥 | Distributed & Network OS | RGPV CS-405 | B.Tech 4th Sem',
  'unit': 'Unit 5',
  'updated_at': '2026-10-18T11:16:53.221588+00:00',
  'year': '2nd Year',
  'youtube_id': 'NCD68uZZCsQ',
  'youtube_url': 'https://www.youtube.com/watch?v=NCD68uZZCsQ'},
 {'created_at': '2026-10-18T11:16:53.221597+00:00',
  'description': '📘 Operating System Unit 4 — Complete One-Shot Revision | RGPV CS-405\n'
                 '\n'
                 'PDF LINK  -https://drive.google.com/file/d/1yNC1KGxOl4kQC_i-EJPw_klUmbNkfAJj/view?usp=sharing\n'
                 '\n'
                 'Preparing for your RGPV B.Tech 4th Semester Operating System exam? This video covers the most '
                 'important concepts from Process Synchronization, Deadlocks and I/O Operations in one complete, '
                 'exam-focused revision.\n'
                 '\n'
                 '🔥 UNIT 4 — TOPICS COVERED:\n'
                 '\n'
                 'Concurrency – Real & Virtual Concurrency\n'
                 'Mutual Exclusion\n'
                 'Critical Section Problem\n'
                 'Process Synchronization\n'
                 'Inter-Process Communication (IPC)\n'
                 'Semaphores – Binary & Counting\n'
                 'WAIT & SIGNAL Operations\n'
                 'Dining Philosophers Problem\n'
                 'Deadlock & Characterization\n'
                 'Deadlock Prevention\n'
                 'Deadlock Avoidance\n'
                 'Banker’s Algorithm 🧮\n'
                 'Deadlock Recovery\n'
                 'Interrupt-Driven I/O\n'
                 'Asynchronous I/O Operations\n'
                 '\n'
                 '🧮 Important Numerical: Banker’s Algorithm\n'
                 '\n'
                 '🎯 Perfect for:\n'
                 '• RGPV CS-405 Exam Preparation\n'
                 '• B.Tech 4th Semester OS Revision\n'
                 '• Unit 4 Complete Revision\n'
                 '• Process Synchronization\n'
                 '• Deadlock Preparation\n'
                 '• Banker’s Algorithm\n'
                 '• Last-Minute Exam Preparation\n'
                 '• PYQ-Oriented Study\n'
                 '\n'
                 '📚 Revise Unit 4 and strengthen the concepts that matter most for your RGPV Operating System exam.\n'
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and complete unit-wise revision. 🔥\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSUnit4 #OSOneShot #OperatingSystemOneShot '
                 '#ProcessSynchronization #Deadlock #BankersAlgorithm #Semaphores #IPC #BTech #BTech4thSem #RGPVExam '
                 '#OSRevision #ExamPreparation #RGPVPYQ #ComputerScience #CSE #EngineeringStudents',
  'notes_url': 'https://drive.google.com/file/d/1yNC1KGxOl4kQC_i-EJPw_klUmbNkfAJj/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'os-unit-4-one-shot-synchronization-deadlocks-io-rgpv-cs-405-btech-4th-sem',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'OS Unit 4 One Shot 🔥 | Synchronization, Deadlocks & I/O | RGPV CS-405 | B.Tech 4th Sem',
  'unit': 'Unit 4',
  'updated_at': '2026-10-18T11:16:53.221598+00:00',
  'year': '2nd Year',
  'youtube_id': 'pnK5UyAdG1k',
  'youtube_url': 'https://www.youtube.com/watch?v=pnK5UyAdG1k'},
 {'created_at': '2026-10-18T11:16:53.221606+00:00',
  'description': '📘 Operating System Unit 3 — Complete One-Shot Revision | RGPV CS-405\n'
                 '\n'
                 'PDF LINK - https://drive.google.com/file/d/1Udc_TvmWGtP5As6w2M1pt3lGiAvxRSnC/view?usp=sharing\n'
                 '\n'
                 'Preparing for your RGPV B.Tech 4th Semester Operating System exam? This video covers the important '
                 'Process Management, CPU Scheduling and Memory Management concepts from Unit 3 in one complete, '
                 'exam-focused revision video. 🚀\n'
                 '\n'
                 '🔥 UNIT 3 — TOPICS COVERED:\n'
                 '\n'
                 'Process Concept & Process States\n'
                 'Process State Transition Diagram\n'
                 'Types of Schedulers\n'
                 'CPU Scheduling Algorithms — FCFS, SJF, SRTF, Priority & Round Robin\n'
                 'CPU Scheduling Numericals using Gantt Chart 🧮\n'
                 'Threads & Thread Control Block (TCB)\n'
                 'Process vs Thread\n'
                 'Paging\n'
                 'Segmentation\n'
                 'Paging vs Segmentation\n'
                 'Segmentation Address Translation 🧮\n'
                 'Virtual Memory\n'
                 'Demand Paging\n'
                 'Page Replacement Algorithms — FIFO, LRU & Optimal 🧮\n'
                 'Thrashing\n'
                 'Overlay\n'
                 'Dynamic Loading\n'
                 'Dynamic Linking\n'
                 'Paged Segmentation\n'
                 'Multiple Processor Scheduling\n'
                 '\n'
                 '🎯 Perfect for:\n'
                 '• RGPV CS-405 Exam Preparation\n'
                 '• B.Tech 4th Semester OS Revision\n'
                 '• Unit 3 Complete Revision\n'
                 '• CPU Scheduling Preparation\n'
                 '• Memory Management Preparation\n'
                 '• Important Numericals\n'
                 '• Last-Minute Exam Preparation\n'
                 '• PYQ-Oriented Study\n'
                 '\n'
                 '🧮 Important Numericals: CPU Scheduling, Gantt Charts, Segmentation Address Translation & Page '
                 'Replacement Algorithms.\n'
                 '\n'
                 '📚 Revise Unit 3, strengthen the important concepts and prepare smarter for your RGPV Operating '
                 'System exam.\n'
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and complete unit-wise revision. 🔥\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSUnit3 #OSOneShot #OperatingSystemOneShot '
                 '#ProcessManagement #CPUScheduling #MemoryManagement #Paging #Segmentation #VirtualMemory #BTech '
                 '#BTech4thSem #RGPVExam #OSRevision #ExamPreparation #RGPVPYQ #ComputerScience #CSE '
                 '#EngineeringStudents',
  'notes_url': 'https://drive.google.com/file/d/1Udc_TvmWGtP5As6w2M1pt3lGiAvxRSnC/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'os-unit-3-one-shot-process-memory-management-rgpv-cs-405-btech-4th-sem',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'OS Unit 3 One Shot 🔥 | Process & Memory Management | RGPV CS-405 | B.Tech 4th Sem',
  'unit': 'Unit 3',
  'updated_at': '2026-10-18T11:16:53.221607+00:00',
  'year': '2nd Year',
  'youtube_id': 'hxOA_u8y_0U',
  'youtube_url': 'https://www.youtube.com/watch?v=hxOA_u8y_0U'},
 {'created_at': '2026-10-18T11:16:53.221615+00:00',
  'description': '📘 Operating System Unit 2 — Complete One-Shot Revision | RGPV CS-405\n'
                 '\n'
                 'PDF LINK - https://drive.google.com/file/d/1O1EAzYVNfBV-CvDXdf9cS1IJqC12fiW8/view?usp=sharing\n'
                 '\n'
                 'Preparing for your RGPV B.Tech 4th Semester Operating System exam? This video covers the complete '
                 'Unit 2: File Systems syllabus in an exam-focused One Shot, perfect for revision before your exam. 🚀\n'
                 '\n'
                 '🔥 UNIT 2 — TOPICS COVERED:\n'
                 '\n'
                 'File Concept, Attributes, Operations & Access Methods\n'
                 'File Allocation Methods — Contiguous, Linked & Indexed\n'
                 'Directory Structures\n'
                 'Disk Organization\n'
                 'Disk Scheduling Algorithms — SSTF, SCAN & LOOK\n'
                 'Disk Scheduling Numericals 🧮\n'
                 'File Protection\n'
                 'System Calls for File Management\n'
                 'Different Modules of a File System\n'
                 'User’s & System Programmer’s View of File System\n'
                 'Tape Organization\n'
                 '\n'
                 '🎯 This video is useful for:\n'
                 '• RGPV CS-405 Exam Preparation\n'
                 '• B.Tech 4th Semester OS Revision\n'
                 '• Unit 2 Complete Revision\n'
                 '• File Systems Preparation\n'
                 '• Disk Scheduling & Important Numericals\n'
                 '• Last-Minute Exam Preparation\n'
                 '• PYQ-Oriented Study\n'
                 '\n'
                 '📚 Revise Unit 2. Focus on important concepts and numericals. Prepare smarter for your RGPV exam.\n'
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and complete unit-wise revision. 🔥\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSUnit2 #OSOneShot #OperatingSystemOneShot '
                 '#FileSystems #FileSystem #DiskScheduling #BTech #BTech4thSem #RGPVExam #OSRevision #ExamPreparation '
                 '#RGPVPYQ #ComputerScience #CSE #EngineeringStudents',
  'notes_url': 'https://drive.google.com/file/d/1O1EAzYVNfBV-CvDXdf9cS1IJqC12fiW8/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'os-unit-2-one-shot-file-systems-complete-revision-rgpv-cs-405-btech-4th-sem',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'OS Unit 2 One Shot 🔥 | File Systems Complete Revision | RGPV CS-405 | B.Tech 4th Sem',
  'unit': 'Unit 2',
  'updated_at': '2026-10-18T11:16:53.221616+00:00',
  'year': '2nd Year',
  'youtube_id': 'sYm12jNPCao',
  'youtube_url': 'https://www.youtube.com/watch?v=sYm12jNPCao'},
 {'created_at': '2026-10-18T11:16:53.221625+00:00',
  'description': '📘 Operating System Unit 1 — Complete One-Shot Revision | RGPV CS-405\n'
                 '\n'
                 'PDF LINK - https://drive.google.com/file/d/1Djrwr0jbdJizXWikijwWoIAIZOTjbyNg/view?usp=sharing\n'
                 '\n'
                 'Preparing for your RGPV B.Tech 4th Semester Operating System exam? This video covers the complete '
                 'Unit 1 syllabus in an exam-focused One Shot, designed for quick and effective revision. 🚀\n'
                 '\n'
                 '🔥 UNIT 1 — TOPICS COVERED:\n'
                 '\n'
                 'Operating System – Definition, Goals, Functions & Types\n'
                 'Evolution of Operating Systems\n'
                 'Desirable Characteristics & Features of OS\n'
                 'Operating System Services\n'
                 'System Calls – Types, Uses & Working\n'
                 'Utility Programs\n'
                 'Buffering & Spooling\n'
                 '\n'
                 '🎯 Perfect for:\n'
                 '• RGPV CS-405 Exam Preparation\n'
                 '• B.Tech 4th Semester Revision\n'
                 '• Last-Minute Exam Preparation\n'
                 '• Unit 1 Complete Revision\n'
                 '• PYQ-Oriented Study\n'
                 '• Quick Syllabus Coverage\n'
                 '\n'
                 '📚 Study smart. Revise important concepts. Prepare for your exam with TSUKOMI PADHAYEGA.\n'
                 '\n'
                 "If you're preparing for Operating System (CS-405), don't forget to check the other unit-wise "
                 'revision videos and important-question videos on the channel.\n'
                 '\n'
                 'Subscribe to TSUKOMI PADHAYEGA for RGPV B.Tech important topics, PYQs, important questions, answers '
                 'and complete revision content. 🔥\n'
                 '\n'
                 'Hashtags\n'
                 '\n'
                 '#OperatingSystem #OS #CS405 #RGPV #RGPVCS405 #OSUnit1 #OSOneShot #OperatingSystemOneShot #BTech '
                 '#BTech4thSem #RGPVExam #RGPVNotes #OSRevision #ExamPreparation #ComputerScience #CSE '
                 '#EngineeringStudents #RGPVPYQ',
  'notes_url': 'https://drive.google.com/file/d/1Djrwr0jbdJizXWikijwWoIAIZOTjbyNg/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'os-unit-1-one-shot-operating-system-complete-revision-rgpv-cs-405-btech-4th-sem',
  'status': 'published',
  'subject': 'Operating Systems',
  'title': 'OS Unit 1 One Shot 🔥 | Operating System Complete Revision | RGPV CS-405 | B.Tech 4th Sem',
  'unit': 'Unit 1',
  'updated_at': '2026-10-18T11:16:53.221626+00:00',
  'year': '2nd Year',
  'youtube_id': 'Kq0zz8fHXRc',
  'youtube_url': 'https://www.youtube.com/watch?v=Kq0zz8fHXRc'},
 {'created_at': '2026-10-18T11:16:53.221635+00:00',
  'description': '📚 COA Top 15 Important Questions | RGPV CS-404 | B.Tech 4th Semester 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF:\n'
                 '👉 https://drive.google.com/file/d/1Xbb-1B9lYY73qbQ7t89ozTJRd2nIXPuV/view?usp=sharing\n'
                 '\n'
                 "Short on time for your COA exam? ⏰ Don't study everything randomly!\n"
                 '\n'
                 'In this video, we cover the Top 15 Important Questions/Topics from Computer Organization & '
                 'Architecture (COA) that you should prioritize for your RGPV CS-404 examination.\n'
                 '\n'
                 'This revision is designed for B.Tech CSE students, RGPV students, engineering students, and anyone '
                 'preparing for Computer Organization & Architecture exams.\n'
                 '\n'
                 '🔥 TOP 15 COA IMPORTANT QUESTIONS\n'
                 '\n'
                 '🟣 UNIT 1 – Control Unit & CPU Organization\n'
                 '\n'
                 '1️⃣ Addressing Modes\n'
                 '2️⃣ Fetch & Execution Cycle\n'
                 '3️⃣ Microprogrammed Control Unit\n'
                 '4️⃣ Hardwired vs Microprogrammed Control Unit\n'
                 '\n'
                 '🟡 UNIT 2 – Computer Arithmetic\n'
                 '\n'
                 '5️⃣ Floating Point Arithmetic\n'
                 '\n'
                 '🔵 UNIT 3 – I/O & Data Transfer\n'
                 '\n'
                 '6️⃣ Direct Memory Access (DMA)\n'
                 "7️⃣ Booth's Algorithm\n"
                 '\n'
                 '🟢 UNIT 4 – Memory Organization\n'
                 '\n'
                 '8️⃣ Cache Mapping Techniques\n'
                 '9️⃣ Cache Performance Improvement\n'
                 '🔟 Memory Hierarchy\n'
                 '\n'
                 '🟠 UNIT 5 – Advanced Computer Architecture\n'
                 '\n'
                 '1️⃣1️⃣ Pipelining\n'
                 '1️⃣2️⃣ Vector Processing\n'
                 '1️⃣3️⃣ Array Processing\n'
                 '1️⃣4️⃣ RISC vs CISC\n'
                 "1️⃣5️⃣ Flynn's Taxonomy\n"
                 '\n'
                 '🎯 WHO SHOULD WATCH THIS?\n'
                 '\n'
                 '✅ RGPV CS-404 Students\n'
                 '✅ B.Tech CSE Students\n'
                 '✅ Computer Organization & Architecture Students\n'
                 '✅ 4th Semester Engineering Students\n'
                 '✅ Students preparing for semester exams\n'
                 '✅ Students doing last-minute revision\n'
                 '✅ Students looking for important COA questions\n'
                 '✅ Students preparing from RGPV PYQs\n'
                 '\n'
                 '🚀 WHY THESE 15?\n'
                 '\n'
                 "If you're short on preparation time, use these topics as your priority list before moving to the "
                 'rest of the syllabus.\n'
                 '\n'
                 '📌 Save this video for revision\n'
                 '📌 Complete these 15 topics first\n'
                 '📌 Then move to remaining topics & PYQs\n'
                 '\n'
                 '\n'
                 'The notes include important concepts and exam-oriented material to help you prepare more '
                 'effectively.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 'RGPV Notes • Important Questions • PYQs • Exam Revision\n'
                 '\n'
                 'If this video helps you prepare:\n'
                 '\n'
                 '👍 LIKE the video\n'
                 '🔔 SUBSCRIBE for more RGPV exam content\n'
                 '📤 SHARE this with your college friends\n'
                 '💬 COMMENT which COA topic you find the hardest!\n'
                 '\n'
                 "🔥 Save it now — you'll need this during revision!\n"
                 '\n'
                 'TSUKOMI PADHAYEGA — Stay Consistent, Stay Ahead! 🚀📚\n'
                 '\n'
                 '#COA #CS404 #RGPV #ComputerOrganization #ComputerArchitecture #COAImportantQuestions #COAPYQ '
                 '#RGPVPYQ #RGPVCS404 #COAExam #COARevision #BTechCSE #BTech4thSem #EngineeringStudents '
                 '#ExamPreparation #RGPVExam #ComputerScience #COAQuestions #ImportantQuestions #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1Xbb-1B9lYY73qbQ7t89ozTJRd2nIXPuV/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-top-15-important-questions-rgpv-cs-404-must-do-before-exam-btech-4th-sem',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': 'COA Top 15 Important Questions 🔥 | RGPV CS-404 | Must Do Before Exam | B.Tech 4th Sem',
  'unit': 'Important Questions',
  'updated_at': '2026-10-18T11:16:53.221636+00:00',
  'year': '2nd Year',
  'youtube_id': 'CMLyUh1xPdY',
  'youtube_url': 'https://www.youtube.com/watch?v=CMLyUh1xPdY'},
 {'created_at': '2026-10-18T11:16:53.221644+00:00',
  'description': '📚 COA CS-404 – COMPLETE 5 UNITS ONE SHOT | RGPV B.Tech Exam Preparation 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF:\n'
                 '👉 https://drive.google.com/drive/folders/1deBo1vc_XKAr8uwyMNXRFd4Fe1RNXQ25?usp=sharing\n'
                 '\n'
                 'Preparing for Computer Organization & Architecture (COA) CS-404? 🔥\n'
                 '\n'
                 'This is the complete COA 5 Units One Shot, covering the entire syllabus from Unit 1 to Unit 5 in one '
                 'exam-focused video.\n'
                 '\n'
                 'Designed especially for RGPV B.Tech students, this video is useful for complete syllabus revision, '
                 'important questions, RGPV PYQs, last-minute preparation, and semester exam revision.\n'
                 '\n'
                 '📚 UNIT 1 — CONTROL UNIT & CPU ORGANIZATION\n'
                 '\n'
                 '✅ Addressing Modes\n'
                 '✅ Instruction Format\n'
                 '✅ Fetch & Execution Cycle\n'
                 '✅ General Register Organization\n'
                 '✅ Hardwired Control Unit\n'
                 '✅ Microprogrammed Control Unit\n'
                 '✅ Hardwired vs Microprogrammed Control Unit\n'
                 '✅ Microinstruction Format\n'
                 '✅ Microprogram Sequencer\n'
                 '✅ Stack Organization\n'
                 '\n'
                 '📚 UNIT 2 — COMPUTER ARITHMETIC\n'
                 '\n'
                 "✅ Booth's Algorithm\n"
                 "✅ Signed 1's & 2's Complement\n"
                 '✅ Signed Binary Addition & Subtraction\n'
                 '✅ Binary Multiplication\n'
                 '✅ Binary Division\n'
                 '✅ Floating Point Representation\n'
                 '✅ Floating Point Arithmetic\n'
                 '✅ Arithmetic Unit\n'
                 '✅ Carry Save Addition\n'
                 '\n'
                 '📚 UNIT 3 — I/O & DATA TRANSFER\n'
                 '\n'
                 '✅ DMA – Direct Memory Access\n'
                 '✅ PCI Bus\n'
                 '✅ SCSI Bus\n'
                 '✅ USB\n'
                 '✅ Serial vs Parallel Transfer\n'
                 '✅ Synchronous vs Asynchronous Transfer\n'
                 '✅ Programmed I/O vs Interrupt I/O vs DMA\n'
                 '✅ Interrupts\n'
                 '✅ Types of Interrupts\n'
                 '\n'
                 '📚 UNIT 4 — MEMORY ORGANIZATION\n'
                 '\n'
                 '✅ Cache Mapping Techniques\n'
                 '✅ Cache Performance Improvement\n'
                 '✅ Memory Hierarchy\n'
                 '✅ Memory Organization\n'
                 '✅ LRU Algorithm\n'
                 '✅ Virtual Memory\n'
                 '✅ Page Replacement\n'
                 '✅ RAM / ROM\n'
                 '✅ Main vs Secondary Memory\n'
                 '\n'
                 '📚 UNIT 5 — ADVANCED COMPUTER ARCHITECTURE\n'
                 '\n'
                 '✅ Pipelining\n'
                 '✅ Vector Processing\n'
                 '✅ Array Processing\n'
                 '✅ RISC vs CISC\n'
                 '✅ Inter-Processor Communication & Synchronization\n'
                 '✅ Multiprocessor Structure\n'
                 '✅ Parallel Processing\n'
                 "✅ Flynn's Taxonomy\n"
                 '\n'
                 "🎯 WHAT YOU'LL GET\n"
                 '\n'
                 '✅ Complete COA CS-404 Syllabus\n'
                 '✅ All 5 Units in One Video\n'
                 '✅ Important Exam Questions\n'
                 '✅ RGPV PYQs + Answers\n'
                 '✅ Easy-to-understand Explanations\n'
                 '✅ Important Diagrams & Concepts\n'
                 '✅ Exam-focused Revision\n'
                 '✅ Useful for Last-Minute Preparation\n'
                 '✅ Complete Semester Revision in One Place\n'
                 '\n'
                 '📌 PERFECT FOR\n'
                 '\n'
                 '🎓 RGPV B.Tech Students\n'
                 '💻 CSE / Computer Science Students\n'
                 '📚 CS-404 Exam Preparation\n'
                 '🔥 Semester Exam Revision\n'
                 '⏰ Last-Minute Revision\n'
                 '📝 RGPV PYQ Preparation\n'
                 '🚀 Students who want to revise COA in one video\n'
                 '\n'
                 '📄 NOTES / PDF:\n'
                 'Download the complete notes, important questions and PYQs from the link provided above/in the '
                 'description.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 'RGPV Notes • Important Questions • PYQs • Complete Revision\n'
                 '\n'
                 'If this video helps you prepare for your COA exam:\n'
                 '\n'
                 '👍 LIKE the video\n'
                 '🔔 SUBSCRIBE to TSUKOMI PADHAYEGA\n'
                 '📤 SHARE it with your college friends\n'
                 '💬 COMMENT your toughest COA topic!\n'
                 '\n'
                 '🔥 Save this video for your final revision!\n'
                 '\n'
                 'TSUKOMI PADHAYEGA — Stay Consistent, Stay Ahead! 🚀📚\n'
                 '\n'
                 '🏷️ HASHTAGS\n'
                 '\n'
                 '#COA #CS404 #RGPV #ComputerOrganization #ComputerArchitecture #COAOneShot #RGPVCS404 #RGPVPYQ '
                 '#COARevision #COAExam #RGPVExam #BTechCSE #EngineeringStudents #ComputerScience #ExamPreparation '
                 '#COACompleteRevision #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/drive/folders/1deBo1vc_XKAr8uwyMNXRFd4Fe1RNXQ25?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-cs-404-complete-5-units-one-shot-rgpv-btech-full-syllabus-revision-pyqs-answers',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': 'COA CS-404 Complete 5 Units One Shot 🔥 | RGPV B.Tech | Full Syllabus Revision | PYQs + Answers',
  'unit': 'Complete Revision',
  'updated_at': '2026-10-18T11:16:53.221645+00:00',
  'year': '2nd Year',
  'youtube_id': 'h9aHz0PUzTg',
  'youtube_url': 'https://www.youtube.com/watch?v=h9aHz0PUzTg'},
 {'created_at': '2026-10-18T11:16:53.221653+00:00',
  'description': '📚 COA Unit 5 – Parallel Processing & Advanced Computer Architecture | Complete One Shot 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF:\n'
                 '👉 https://drive.google.com/file/d/1J8v_3NIkeci_yui5zh2P5nTETKgbMvd3/view?usp=sharing\n'
                 '\n'
                 'In this video, we will cover Computer Organization & Architecture (COA) Unit 5 completely in an easy '
                 'and exam-focused way for RGPV CS-404.\n'
                 '\n'
                 'This COA Unit 5 One Shot is specially designed for RGPV B.Tech Computer Science students preparing '
                 'for semester examinations, covering important concepts along with RGPV Previous Year Questions '
                 '(PYQs) and their answers.\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 'Pipelining\n'
                 'Vector Processing\n'
                 'Array Processing\n'
                 'RISC vs CISC\n'
                 'Inter-Processor Communication & Synchronization\n'
                 'Multiprocessor Structure\n'
                 'Parallel Processing\n'
                 "Flynn's Taxonomy\n"
                 'Important Diagrams & Exam Concepts\n'
                 'RGPV PYQ Questions + Answers\n'
                 '\n'
                 'The complete unit is explained in simple and easy-to-understand language, with a strong focus on '
                 'important questions from the RGPV examination point of view.\n'
                 '\n'
                 '🎯 Why Watch This One Shot?\n'
                 '\n'
                 '✅ Complete Unit 5 Revision\n'
                 '✅ RGPV Exam Focused\n'
                 '✅ Important Questions Covered\n'
                 '✅ RGPV PYQs + Answers\n'
                 '✅ Pipelining Explained\n'
                 '✅ RISC vs CISC Explained\n'
                 '✅ Multiprocessor & Parallel Processing Covered\n'
                 "✅ Flynn's Taxonomy Explained\n"
                 '✅ Important Diagrams & Concepts\n'
                 '✅ Easy-to-understand explanations\n'
                 '✅ Useful for Last-Minute Revision\n'
                 '✅ Complete Unit in One Video\n'
                 '\n'
                 '📄 Notes containing important questions, RGPV PYQs and answers are available through the download '
                 'link above.\n'
                 '\n'
                 'If this video helps you prepare:\n'
                 '\n'
                 '👍 LIKE the video\n'
                 '🔔 SUBSCRIBE to TSUKOMI PADHAYEGA\n'
                 '📤 SHARE it with your college friends\n'
                 '\n'
                 'TSUKOMI PADHAYEGA — Stay Consistent, Stay Ahead! 🚀📚\n'
                 '\n'
                 '🏷️ Hashtags\n'
                 '\n'
                 '#COA #CS404 #RGPV #COAUnit5 #RGPVPYQ #ComputerOrganization #ComputerArchitecture #COAOneShot '
                 '#RGPVCS404 #Pipelining #VectorProcessing #RISCvsCISC #ParallelProcessing #Multiprocessor '
                 '#FlynnTaxonomy #BTech #ExamPreparation #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1J8v_3NIkeci_yui5zh2P5nTETKgbMvd3/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-unit-5-one-shot-pipelining-risc-vs-cisc-parallel-processing-rgpv-pyqs-cs-404',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': 'COA Unit 5 One Shot | Pipelining, RISC vs CISC, Parallel Processing | RGPV PYQs | CS-404',
  'unit': 'Unit 5',
  'updated_at': '2026-10-18T11:16:53.221654+00:00',
  'year': '2nd Year',
  'youtube_id': 'izqkUj0JLd0',
  'youtube_url': 'https://www.youtube.com/watch?v=izqkUj0JLd0'},
 {'created_at': '2026-10-18T11:16:53.221661+00:00',
  'description': '📚 COA Unit 4 – Memory Organization | Complete One Shot 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF:\n'
                 '👉 https://drive.google.com/file/d/1XxZe2xvdWAGqvYoVhnI1SMq7eDJ5ZDs9/view?usp=sharing\n'
                 '\n'
                 'In this video, we will cover Computer Organization & Architecture (COA) Unit 4 completely in an easy '
                 'and exam-focused way for RGPV CS-404.\n'
                 '\n'
                 'This COA Unit 4 One Shot is specially designed for RGPV B.Tech Computer Science students preparing '
                 'for semester examinations, covering important memory-related concepts along with RGPV Previous Year '
                 'Questions (PYQs) and their answers.\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 'Memory Hierarchy\n'
                 'Memory Organization\n'
                 'Cache Memory\n'
                 'Cache Mapping Techniques\n'
                 'Direct Mapping\n'
                 'Fully Associative Mapping\n'
                 'Set Associative Mapping\n'
                 'Cache Performance Improvement\n'
                 'LRU Algorithm\n'
                 'Virtual Memory\n'
                 'Page Replacement Algorithms\n'
                 'RAM and ROM\n'
                 'Types of RAM and ROM\n'
                 'Main Memory vs Secondary Memory\n'
                 'Important Diagrams & Exam Concepts\n'
                 'RGPV PYQ Questions + Answers\n'
                 '\n'
                 'The complete unit is explained in simple and easy-to-understand language, with a strong focus on '
                 'important questions from the RGPV examination point of view.\n'
                 '\n'
                 '🎯 Why Watch This One Shot?\n'
                 '\n'
                 '✅ Complete Unit 4 Revision\n'
                 '✅ RGPV Exam Focused\n'
                 '✅ Important Questions Covered\n'
                 '✅ RGPV PYQs + Answers\n'
                 '✅ Cache Mapping Explained\n'
                 '✅ LRU & Page Replacement Explained\n'
                 '✅ Virtual Memory & Memory Hierarchy\n'
                 '✅ Easy-to-understand explanations\n'
                 '✅ Useful for Last-Minute Revision\n'
                 '✅ Complete Unit in One Video\n'
                 '\n'
                 '📄 Notes containing important questions, RGPV PYQs and answers are available through the download '
                 'link above.\n'
                 '\n'
                 'If this video helps you prepare:\n'
                 '\n'
                 '👍 LIKE the video\n'
                 '🔔 SUBSCRIBE to TSUKOMI PADHAYEGA\n'
                 '📤 SHARE it with your college friends\n'
                 '\n'
                 'TSUKOMI PADHAYEGA — Stay Consistent, Stay Ahead! 🚀📚\n'
                 '\n'
                 '🏷️ Hashtags\n'
                 '\n'
                 '#COA #CS404 #RGPV #COAUnit4 #RGPVPYQ #ComputerOrganization #ComputerArchitecture #COAOneShot '
                 '#RGPVCS404 #MemoryOrganization #CacheMemory #CacheMapping #LRU #VirtualMemory #PageReplacement #RAM '
                 '#ROM #BTech #ExamPreparation #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1XxZe2xvdWAGqvYoVhnI1SMq7eDJ5ZDs9/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-unit-4-one-shot-memory-organization-cache-rgpv-pyqs-answers-cs-404',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': 'COA Unit 4 One Shot | Memory Organization & Cache | RGPV PYQs + Answers | CS-404',
  'unit': 'Unit 4',
  'updated_at': '2026-10-18T11:16:53.221662+00:00',
  'year': '2nd Year',
  'youtube_id': 'kzvrNNqepAk',
  'youtube_url': 'https://www.youtube.com/watch?v=kzvrNNqepAk'},
 {'created_at': '2026-10-18T11:16:53.221669+00:00',
  'description': 'COA Unit 3 – Computer Arithmetic | Complete One Shot 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF:\n'
                 '👉 https://drive.google.com/file/d/1HAn-FYxKDiYh8KYCkKfCUokCCRlv30Uc/view?usp=sharing\n'
                 '\n'
                 'In this video, we will cover Computer Organization & Architecture (COA) Unit 3 completely in an easy '
                 'and exam-focused way for RGPV CS-404.\n'
                 '\n'
                 'This COA Unit 3 One Shot is specially designed for RGPV B.Tech Computer Science students preparing '
                 'for semester examinations.\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 'Addition and Subtraction\n'
                 "2's Complement Representation\n"
                 'Signed Addition and Subtraction\n'
                 'Binary Multiplication\n'
                 'Binary Division\n'
                 "Booth's Multiplication Algorithm\n"
                 'Division Operation\n'
                 'Floating Point Representation\n'
                 'Floating Point Arithmetic\n'
                 'Design of Arithmetic Unit\n'
                 'Important exam concepts and explanations\n'
                 'RGPV PYQ Questions + Answers\n'
                 '\n'
                 'The complete unit is explained in simple and easy-to-understand language, with an emphasis on '
                 'questions that are important from the RGPV examination point of view.\n'
                 '\n'
                 '🎯 Why Watch This One Shot?\n'
                 '\n'
                 '✅ Complete Unit 3 Revision\n'
                 '✅ RGPV Exam Focused\n'
                 '✅ Important Questions Covered\n'
                 '✅ RGPV PYQs + Answers\n'
                 "✅ Booth's Algorithm Explained\n"
                 '✅ Easy-to-understand explanations\n'
                 '✅ Useful for Last-Minute Revision\n'
                 '✅ Complete Unit in One Video\n'
                 '\n'
                 '#COA #ComputerOrganizationAndArchitecture #COAUnit3 #RGPV #RGPVCS404 #CS404 #ComputerArithmetic '
                 '#BoothsAlgorithm #FloatingPointArithmetic #RGPVExam #COAOneShot #RGPVPYQ #BTechCSE '
                 '#EngineeringStudents #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1HAn-FYxKDiYh8KYCkKfCUokCCRlv30Uc/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-unit-3-one-shot-computer-arithmetic-booths-algorithm-floating-point-rgpv-cs-404',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': "COA Unit 3 One Shot | Computer Arithmetic | Booth's Algorithm, Floating Point | RGPV CS-404",
  'unit': 'Unit 3',
  'updated_at': '2026-10-18T11:16:53.221670+00:00',
  'year': '2nd Year',
  'youtube_id': 'vp8geYIKmlw',
  'youtube_url': 'https://www.youtube.com/watch?v=vp8geYIKmlw'},
 {'created_at': '2026-10-18T11:16:53.221677+00:00',
  'description': '📚 COA Unit 2 – Computer Arithmetic | Complete One Shot 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF: '
                 'https://drive.google.com/file/d/1a4zGufHnmfkS8wBn9Q-772ludwALM50S/view?usp=sharing\n'
                 '\n'
                 'In this video, we will cover Computer Organization & Architecture (COA) Unit 2 completely in an easy '
                 'and exam-focused way for RGPV CS-404.\n'
                 '\n'
                 'This COA Unit 2 One Shot is specially designed for RGPV B.Tech Computer Science students preparing '
                 'for semester examinations, with important concepts, RGPV Previous Year Questions (PYQs) and their '
                 'answers for quick revision.\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 'Booth’s Algorithm\n'
                 'Signed 1’s & 2’s Complement\n'
                 'Floating Point Arithmetic\n'
                 'Signed Binary Addition & Subtraction\n'
                 'Arithmetic Unit\n'
                 'Carry Save Addition\n'
                 'Important exam concepts and explanations\n'
                 'RGPV PYQ Questions + Answers\n'
                 '\n'
                 'The complete unit is explained in simple and easy-to-understand language, with a strong focus on '
                 'important questions from the RGPV examination point of view.\n'
                 '\n'
                 '🎯 Why Watch This One Shot?\n'
                 '\n'
                 '✅ Complete Unit 2 Revision\n'
                 '✅ RGPV Exam Focused\n'
                 '✅ Important Questions Covered\n'
                 '✅ RGPV PYQs + Answers\n'
                 '✅ Booth’s Algorithm Explained\n'
                 '✅ Easy-to-understand explanations\n'
                 '✅ Useful for Last-Minute Revision\n'
                 '✅ Complete Unit in One Video\n'
                 '\n'
                 '📄 Notes containing RGPV PYQs and answers are available through the download link above.\n'
                 '\n'
                 'If this video helps you prepare:\n'
                 '\n'
                 '👍 LIKE the video\n'
                 '🔔 SUBSCRIBE to TSUKOMI PADHAYEGA\n'
                 '📤 SHARE it with your college friends\n'
                 '\n'
                 'TSUKOMI PADHAYEGA — Stay Consistent, Stay Ahead! 🚀📚\n'
                 '\n'
                 '🏷️ Hashtags\n'
                 '\n'
                 '#COA #CS404 #RGPV #COAUnit2 #RGPVPYQ #ComputerOrganization #ComputerArchitecture #COAOneShot '
                 '#RGPVCS404 #BTech #EngineeringStudents #ExamPreparation #BoothsAlgorithm #ComputerArithmetic '
                 '#RGPVExam',
  'notes_url': 'https://drive.google.com/file/d/1a4zGufHnmfkS8wBn9Q-772ludwALM50S/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-unit-2-complete-one-shot-cs-404-rgpv-pyqs-answers-computer-organization-architecture',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': 'COA Unit 2 Complete One Shot | CS-404 | RGPV PYQs + Answers | Computer Organization & Architecture',
  'unit': 'Unit 2',
  'updated_at': '2026-10-18T11:16:53.221679+00:00',
  'year': '2nd Year',
  'youtube_id': '2t4AQs7SjAY',
  'youtube_url': 'https://www.youtube.com/watch?v=2t4AQs7SjAY'},
 {'created_at': '2026-10-18T11:16:53.221686+00:00',
  'description': '📚 COA Unit 1 – Computer Organization & Architecture | Complete One Shot 🔥\n'
                 '\n'
                 '📄 DOWNLOAD NOTES / PDF:  '
                 'https://drive.google.com/file/d/1iWYPmx0JLDtsdsbeRZ-o7oG5TTM-xkef/view?usp=sharing\n'
                 'In this video, we will cover Computer Organization & Architecture (COA) Unit 1 completely in an easy '
                 'and exam-focused way for RGPV CS-404.\n'
                 '\n'
                 'This COA Unit 1 One Shot is specially designed for RGPV B.Tech Computer Science students preparing '
                 'for their semester examinations, covering important concepts, diagrams, RGPV Previous Year Questions '
                 '(PYQs) and their answers.\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 'Addressing Modes\n'
                 'Instruction Format\n'
                 'Fetch & Execution Cycle\n'
                 'General Register Organization\n'
                 'Hardwired Control Unit\n'
                 'Microprogrammed Control Unit\n'
                 'Hardwired vs Microprogrammed Control Unit\n'
                 'Microinstruction Format\n'
                 'Microprogram Sequencer\n'
                 'Stack Organization\n'
                 'Important diagrams and exam concepts\n'
                 'RGPV PYQ Questions + Answers\n'
                 '\n'
                 'The complete unit is explained in simple and easy-to-understand language, with a strong focus on '
                 'important questions from the RGPV examination point of view.\n'
                 '\n'
                 '🎯 Why Watch This One Shot?\n'
                 '\n'
                 '✅ Complete Unit 1 Revision\n'
                 '✅ RGPV Exam Focused\n'
                 '✅ Important Questions Covered\n'
                 '✅ RGPV PYQs + Answers\n'
                 '✅ Important Diagrams & Concepts\n'
                 '✅ Easy-to-understand explanations\n'
                 '✅ Useful for Last-Minute Revision\n'
                 '✅ Complete Unit in One Video\n'
                 '\n'
                 '📄 Notes containing important questions, RGPV PYQs and answers are available through the download '
                 'link above.\n'
                 '\n'
                 'If this video helps you prepare:\n'
                 '\n'
                 '👍 LIKE the video\n'
                 '🔔 SUBSCRIBE to TSUKOMI PADHAYEGA\n'
                 '📤 SHARE it with your college friends\n'
                 '\n'
                 'TSUKOMI PADHAYEGA — Stay Consistent, Stay Ahead! 🚀📚\n'
                 '\n'
                 '🏷️ Hashtags\n'
                 '\n'
                 '#COA #CS404 #RGPV #COAUnit1 #RGPVPYQ #ComputerOrganization #ComputerArchitecture #COAOneShot '
                 '#RGPVCS404 #BTech #EngineeringStudents #ExamPreparation #AddressingModes #ControlUnit '
                 '#Microprogramming #RGPVExam',
  'notes_url': 'https://drive.google.com/file/d/1iWYPmx0JLDtsdsbeRZ-o7oG5TTM-xkef/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'coa-unit-1-complete-one-shot-rgpv-cs-404-complete-notes-pyq-questions-answers',
  'status': 'published',
  'subject': 'Computer Organization & Architecture',
  'title': 'COA Unit 1 Complete One Shot | RGPV CS-404 | Complete Notes + PYQ Questions & Answers',
  'unit': 'Unit 1',
  'updated_at': '2026-10-18T11:16:53.221687+00:00',
  'year': '2nd Year',
  'youtube_id': 'cnEnXjeZO8U',
  'youtube_url': 'https://www.youtube.com/watch?v=cnEnXjeZO8U'},
 {'created_at': '2026-10-18T11:16:53.221694+00:00',
  'description': '📄 DOWNLOAD COMPLETE SOFTWARE ENGINEERING NOTES — FREE PDF:\n'
                 '🔗 https://drive.google.com/drive/folders/1DOdOYJCQp0o1EGiSCW3igAn9HqTfaGTt?usp=sharing\n'
                 '\n'
                 '🔥 Software Engineering One Shot | All 5 Units Complete Revision | RGPV CS-403\n'
                 '\n'
                 'Preparing for RGPV B.Tech 4th Semester Software Engineering (CS-403)?\n'
                 'This video covers ALL 5 UNITS of Software Engineering in one complete revision video, designed '
                 'especially for last-minute exam preparation, important questions and quick syllabus revision. 🎯\n'
                 '\n'
                 '📚 COMPLETE SYLLABUS COVERED:\n'
                 '\n'
                 '🟡 UNIT 1 — Introduction & Software Process\n'
                 '\n'
                 'Software Engineering\n'
                 'Software Crisis\n'
                 'SDLC\n'
                 'Waterfall Model\n'
                 'Prototyping Model\n'
                 'Spiral Model\n'
                 'Component Assembly Model\n'
                 'Agile Process\n'
                 'CMM\n'
                 'Software Product vs Software Process\n'
                 'Software Metrics\n'
                 '\n'
                 '🟢 UNIT 2 — Requirement Engineering\n'
                 '\n'
                 'Requirement Engineering\n'
                 'Requirement Elicitation\n'
                 'Requirement Analysis\n'
                 'Requirement Validation\n'
                 'Requirement Traceability\n'
                 'Use Case Modeling\n'
                 'Use Case Diagram\n'
                 'Function-Oriented Analysis\n'
                 'Object-Oriented Analysis\n'
                 'Function-Oriented vs Object-Oriented Analysis\n'
                 '\n'
                 '🔵 UNIT 3 — Software Design\n'
                 '\n'
                 'Software Design Process\n'
                 'Design Principles\n'
                 'Design Concepts\n'
                 'Architectural Design\n'
                 'Design Notations\n'
                 'Structure Chart\n'
                 'Data Flow Diagram (DFD)\n'
                 'Software Design Strategies\n'
                 'Function-Oriented Design\n'
                 'Object-Oriented Design\n'
                 'Function-Oriented vs Object-Oriented Design\n'
                 '\n'
                 '🔴 UNIT 4 — Software Testing\n'
                 '\n'
                 'Coding Standards\n'
                 'Code Review\n'
                 'Software Testing\n'
                 'Black Box Testing\n'
                 'White Box Testing\n'
                 'Unit Testing\n'
                 'Integration Testing\n'
                 'System Testing\n'
                 'Validation Testing\n'
                 'Debugging\n'
                 'Verification vs Validation\n'
                 'Static & Dynamic Analysis\n'
                 'Test Plan & Metrics\n'
                 'OOAD\n'
                 '\n'
                 '🟣 UNIT 5 — Software Maintenance\n'
                 '\n'
                 'Software Maintenance\n'
                 'Types of Maintenance\n'
                 'Software Re-engineering\n'
                 'Reverse Engineering\n'
                 'Software Reuse\n'
                 'CASE Tools\n'
                 'Software Configuration Management (SCM)\n'
                 'Version Control\n'
                 'Change Management\n'
                 'Software Metrics\n'
                 'Software Maintenance Process\n'
                 '🎯 PERFECT FOR:\n'
                 '\n'
                 '✅ RGPV CS-403 Exam Preparation\n'
                 '✅ B.Tech 4th Semester\n'
                 '✅ Software Engineering One Shot\n'
                 '✅ All 5 Units Revision\n'
                 '✅ Important Questions\n'
                 '✅ RGPV PYQ Preparation\n'
                 '✅ Last-Minute Revision\n'
                 '✅ Quick Syllabus Revision\n'
                 '✅ Semester Exams\n'
                 '\n'
                 '📄 FREE PDF NOTES:\n'
                 'Complete notes used for this revision are available through the PDF link above.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 '\n'
                 'RGPV Notes • PYQs • Important Questions • Complete Revision • Exam Preparation\n'
                 '\n'
                 '👍 Like the video\n'
                 '💬 Comment your doubts\n'
                 '📤 Share with your friends\n'
                 '🔔 Subscribe to TSUKOMI PADHAYEGA\n'
                 '\n'
                 '#SoftwareEngineering #RGPV #CS403 #RGPVCS403 #OneShot #SoftwareEngineeringOneShot #RGPVNotes '
                 '#RGPVPYQ #BTech #BTechCSE #4thSem #ExamPreparation #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/drive/folders/1DOdOYJCQp0o1EGiSCW3igAn9HqTfaGTt?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'software-engineering-one-shot-all-5-units-complete-revision-rgpv-cs-403-4th-sem',
  'status': 'published',
  'subject': 'Software Engineering',
  'title': 'Software Engineering One Shot | All 5 Units Complete Revision | RGPV CS-403 | 4th Sem',
  'unit': 'Complete Revision',
  'updated_at': '2026-10-18T11:16:53.221695+00:00',
  'year': '2nd Year',
  'youtube_id': 'UxTklWTfNEI',
  'youtube_url': 'https://www.youtube.com/watch?v=UxTklWTfNEI'},
 {'created_at': '2026-10-18T11:16:53.221702+00:00',
  'description': '📄 Download Complete Notes (FREE PDF):\n'
                 '🔗 https://drive.google.com/file/d/1mmGJohSnBKwr55rbiEBc04sIV_8oJd8_/view?usp=sharing\n'
                 '\n'
                 '📘 Software Engineering Unit 5 Complete Notes | Software Maintenance | RGPV CS-403\n'
                 '\n'
                 'In this video, we cover Software Engineering Unit 5 – Software Maintenance in a simple, detailed and '
                 'exam-oriented way for RGPV B.Tech 4th Semester CS-403 students. 🎯\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 '\n'
                 '✅ Software Maintenance\n'
                 '✅ Types of Software Maintenance\n'
                 '✅ Software Re-engineering\n'
                 '✅ Reverse Engineering\n'
                 '✅ Software Reuse\n'
                 '✅ CASE Tools\n'
                 '✅ Software Configuration Management (SCM)\n'
                 '✅ Version Control\n'
                 '✅ Change Management\n'
                 '✅ Software Metrics\n'
                 '✅ Software Maintenance Process\n'
                 '\n'
                 '🎯 Perfect For:\n'
                 '\n'
                 '📌 RGPV CS-403 Software Engineering\n'
                 '📌 B.Tech 4th Semester Students\n'
                 '📌 Software Maintenance Exam Preparation\n'
                 '📌 RGPV Important Questions\n'
                 '📌 RGPV PYQ Preparation\n'
                 '📌 Last-Minute Revision\n'
                 '📌 Assignment & Viva Preparation\n'
                 '\n'
                 '📄 FREE PDF NOTES:\n'
                 'Get the complete notes used in this video from the PDF link above.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 '\n'
                 'RGPV Notes • Important Questions • PYQs • Complete Revision • Exam Preparation\n'
                 '\n'
                 '👍 Like the video\n'
                 '💬 Comment your doubts\n'
                 '📤 Share with your classmates\n'
                 '🔔 Subscribe for more RGPV content!\n'
                 '\n'
                 '#SoftwareEngineering #RGPV #CS403 #SoftwareMaintenance #RGPVCS403 #SoftwareReengineering #SCM '
                 '#ReverseEngineering #BTech #RGPVNotes #ExamPreparation #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1mmGJohSnBKwr55rbiEBc04sIV_8oJd8_/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'software-engineering-unit-5-important-questions-software-maintenance-rgpv-cs-403',
  'status': 'published',
  'subject': 'Software Engineering',
  'title': 'Software Engineering Unit 5 Important Questions | Software Maintenance | RGPV CS-403',
  'unit': 'Unit 5',
  'updated_at': '2026-10-18T11:16:53.221703+00:00',
  'year': '2nd Year',
  'youtube_id': '2LA3s5j_SX0',
  'youtube_url': 'https://www.youtube.com/watch?v=2LA3s5j_SX0'},
 {'created_at': '2026-10-18T11:16:53.221709+00:00',
  'description': '📄 Download Complete Notes (FREE PDF):\n'
                 '🔗 https://drive.google.com/file/d/1TXY6ywYqScwTNyti_r5VXiAfZYnXVHHb/view?usp=sharing\n'
                 '\n'
                 '📘 Software Engineering Unit 4 Complete Notes | Software Testing | RGPV CS-403\n'
                 '\n'
                 'In this video, we cover Software Engineering Unit 4 – Software Testing in a simple, detailed and '
                 'exam-oriented way for RGPV B.Tech 4th Semester CS-403 students. 🎯\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 '\n'
                 '✅ Coding Standards\n'
                 '✅ Code Review\n'
                 '✅ Software Testing\n'
                 '✅ Black Box Testing\n'
                 '✅ White Box Testing\n'
                 '✅ Unit Testing\n'
                 '✅ Integration Testing\n'
                 '✅ System Testing\n'
                 '✅ Validation Testing\n'
                 '✅ Debugging\n'
                 '✅ Verification vs Validation\n'
                 '\n'
                 '🎯 Perfect For:\n'
                 '\n'
                 '📌 RGPV CS-403 Software Engineering\n'
                 '📌 B.Tech 4th Semester Students\n'
                 '📌 Software Testing Exam Preparation\n'
                 '📌 RGPV Important Questions\n'
                 '📌 RGPV PYQ Preparation\n'
                 '📌 Last-Minute Revision\n'
                 '📌 Assignment & Viva Preparation\n'
                 '\n'
                 '📄 FREE PDF NOTES:\n'
                 'Get the complete notes used in this video from the PDF link above.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 '\n'
                 'RGPV Notes • Important Questions • PYQs • Complete Revision • Exam Preparation\n'
                 '\n'
                 '👍 Like the video\n'
                 '💬 Comment your doubts\n'
                 '📤 Share with your classmates\n'
                 '🔔 Subscribe for more RGPV content!',
  'notes_url': 'https://drive.google.com/file/d/1TXY6ywYqScwTNyti_r5VXiAfZYnXVHHb/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'software-engineering-unit-4-important-questions-software-testing-rgpv-cs-403',
  'status': 'published',
  'subject': 'Software Engineering',
  'title': 'Software Engineering Unit 4 Important Questions | Software Testing | RGPV CS-403',
  'unit': 'Unit 4',
  'updated_at': '2026-10-18T11:16:53.221710+00:00',
  'year': '2nd Year',
  'youtube_id': '3c0xCe-wt84',
  'youtube_url': 'https://www.youtube.com/watch?v=3c0xCe-wt84'},
 {'created_at': '2026-10-18T11:16:53.221716+00:00',
  'description': '📄 FREE PDF NOTES:\n'
                 '🔗 https://drive.google.com/file/d/1BKDhAkDEhm1n3vg-16w-H3_FY8aFF7q9/view?usp=sharing\n'
                 '\n'
                 '📘 Software Engineering Unit 3 Complete Notes | RGPV CS-403\n'
                 '\n'
                 'In this video, we cover Software Engineering Unit 3 – Software Design in a simple and exam-oriented '
                 'way for RGPV B.Tech 4th Semester CS-403 students.\n'
                 '\n'
                 'This video is useful for RGPV University Exam Preparation, Important Questions, PYQ Preparation, '
                 'Assignments, Viva, and Last-Minute Revision. 🎯\n'
                 '\n'
                 '📚 UNIT 3 TOPICS COVERED:\n'
                 '\n'
                 '✅ Software Design Process\n'
                 '✅ Design Principles\n'
                 '✅ Design Concepts\n'
                 '✅ Architectural Design\n'
                 '✅ Design Notations\n'
                 '✅ Structure Chart\n'
                 '✅ Data Flow Diagram (DFD)\n'
                 '✅ Software Design Strategies\n'
                 '✅ Function-Oriented Design\n'
                 '✅ Object-Oriented Design\n'
                 '✅ Function-Oriented vs Object-Oriented Design\n'
                 '\n'
                 '🎯 PERFECT FOR:\n'
                 '\n'
                 '• RGPV CS-403 Software Engineering\n'
                 '• B.Tech 4th Semester Students\n'
                 '• RGPV University Exams\n'
                 '• Software Engineering Important Questions\n'
                 '• Software Design Preparation\n'
                 '• PYQ-Based Learning\n'
                 '• Last-Minute Revision\n'
                 '• Assignment & Viva Preparation\n'
                 '\n'
                 '📌 FREE PDF:\n'
                 'Complete notes used in this video are available through the link above.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 '\n'
                 'RGPV Notes • Important Questions • PYQs • Exam Preparation\n'
                 '\n'
                 '👍 Like the video\n'
                 '💬 Comment your doubts\n'
                 '📤 Share with your classmates\n'
                 '🔔 Subscribe for more RGPV exam content!\n'
                 '\n'
                 '#SoftwareEngineering #RGPV #CS403 #SoftwareDesign #RGPVCS403 #DFD #ObjectOrientedDesign #BTech '
                 '#RGPVNotes #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1BKDhAkDEhm1n3vg-16w-H3_FY8aFF7q9/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'software-engineering-unit-3-complete-notes-software-design-rgpv-cs-403-4th-sem',
  'status': 'published',
  'subject': 'Software Engineering',
  'title': 'Software Engineering Unit 3 Complete Notes | Software Design | RGPV CS-403 | 4th Sem',
  'unit': 'Unit 3',
  'updated_at': '2026-10-18T11:16:53.221717+00:00',
  'year': '2nd Year',
  'youtube_id': 'tXYbYiw8NVM',
  'youtube_url': 'https://www.youtube.com/watch?v=tXYbYiw8NVM'},
 {'created_at': '2026-10-18T11:16:53.221725+00:00',
  'description': '📄 Download Complete Notes (FREE PDF):\n'
                 '🔗 \n'
                 'https://drive.google.com/file/d/1ohfcU2iH1EDIn39k4YvS-SJjzsWaH4Yy/view?usp=sharing\n'
                 '\n'
                 '📘 Software Engineering Unit 2 Complete Notes | RGPV CS-403\n'
                 '\n'
                 'In this video, we cover Software Engineering Unit 2 in a simple, exam-oriented way for RGPV B.Tech '
                 '4th Semester CS-403 students.\n'
                 '\n'
                 'This video is useful for RGPV University Exam Preparation, Important Questions, PYQ Preparation, '
                 'Assignments, and Last-Minute Revision. 🎯\n'
                 '\n'
                 '📚 Topics Covered:\n'
                 '\n'
                 '✅ Requirement Engineering\n'
                 '✅ Requirement Elicitation\n'
                 '✅ Requirement Analysis\n'
                 '✅ Requirement Validation\n'
                 '✅ Requirement Traceability\n'
                 '✅ Use Case Modeling\n'
                 '✅ Use Case Diagram\n'
                 '✅ Function-Oriented Analysis\n'
                 '✅ Object-Oriented Analysis\n'
                 '✅ Function-Oriented vs Object-Oriented Analysis\n'
                 '\n'
                 '🎯 This Video Is Perfect For:\n'
                 '\n'
                 '• RGPV CS-403 Software Engineering\n'
                 '• B.Tech 4th Semester Students\n'
                 '• RGPV University Exams\n'
                 '• Software Engineering Important Questions\n'
                 '• PYQ-Based Preparation\n'
                 '• Last-Minute Revision\n'
                 '• Assignment & Viva Preparation\n'
                 '\n'
                 '📌 FREE PDF NOTES:\n'
                 'The complete notes used in this video are available through the link above.\n'
                 '\n'
                 '🎓 TSUKOMI PADHAYEGA\n'
                 '\n'
                 'Get RGPV Notes, Important Questions, PYQs, Revision Videos & Exam Preparation content.\n'
                 '\n'
                 '👍 Like the video\n'
                 '💬 Comment your doubts\n'
                 '📤 Share with your classmates\n'
                 '🔔 Subscribe for more RGPV exam content!\n'
                 '\n'
                 '#SoftwareEngineering #RGPV #CS403 #RequirementEngineering #RGPVCS403 #SoftwareEngineeringRGPV #BTech '
                 '#RGPVNotes #ExamPreparation #TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1ohfcU2iH1EDIn39k4YvS-SJjzsWaH4Yy/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'software-engineering-unit-2-complete-notes-requirement-engineering-rgpv-cs-403',
  'status': 'published',
  'subject': 'Software Engineering',
  'title': 'Software Engineering Unit 2 Complete Notes | Requirement Engineering | RGPV CS-403',
  'unit': 'Unit 2',
  'updated_at': '2026-10-18T11:16:53.221727+00:00',
  'year': '2nd Year',
  'youtube_id': 'QugOsveKh5A',
  'youtube_url': 'https://www.youtube.com/watch?v=QugOsveKh5A'},
 {'created_at': '2026-10-18T11:16:53.221733+00:00',
  'description': '📘 Software Engineering Unit 1 Complete Notes | RGPV CS-403\n'
                 '\n'
                 '📄 Download Complete Notes (PDF):\n'
                 '🔗https://drive.google.com/file/d/1T4fw3VRFZMCLALQn4O6X8QESfNq86yVl/view?usp=sharing\n'
                 '\n'
                 'Welcome to TSUKOMI PADHAYEGA! 🎓\n'
                 '\n'
                 "In this video, you'll get complete Unit 1 notes for Software Engineering (CS-403) based on the RGPV "
                 'B.Tech 4th Semester syllabus. These notes are prepared in a simple, exam-oriented format to help you '
                 'score better in university exams.\n'
                 '\n'
                 '📚 Topics Covered\n'
                 '\n'
                 '✔ Introduction to Software Engineering\n'
                 '✔ Software Crisis\n'
                 '✔ Software Characteristics\n'
                 '✔ Software Process\n'
                 '✔ Software Development Life Cycle (SDLC)\n'
                 '✔ Waterfall Model\n'
                 '✔ Prototyping Model\n'
                 '✔ Spiral Model\n'
                 '✔ Component Assembly Model\n'
                 '✔ Agile Process\n'
                 '✔ Capability Maturity Model (CMM)\n'
                 '✔ Software Product vs Software Process\n'
                 '✔ Software Metrics\n'
                 '\n'
                 '🎯 Perfect For\n'
                 'RGPV B.Tech 4th Semester Students\n'
                 'University Exam Preparation\n'
                 'Assignment & Viva Preparation\n'
                 'PYQ-Based Learning\n'
                 'Last-Minute Revision\n'
                 '\n'
                 'If this video helped you:\n'
                 '\n'
                 '👍 Like the video\n'
                 '💬 Comment your doubts or suggestions\n'
                 '📢 Share it with your classmates\n'
                 '🔔 Subscribe to TSUKOMI PADHAYEGA for more RGPV Notes, PYQ Solutions, and Complete Exam Revision '
                 'Videos.\n'
                 '\n'
                 'Thank you for watching, and all the best for your exams! 🚀\n'
                 '\n'
                 '#SoftwareEngineering #RGPV #CS403 #SDLC #WaterfallModel #Agile #SpiralModel #Engineering #BTech '
                 '#TSUKOMIPADHAYEGA',
  'notes_url': 'https://drive.google.com/file/d/1T4fw3VRFZMCLALQn4O6X8QESfNq86yVl/view?usp=sharing',
  'published': True,
  'semester': '4th Semester',
  'slug': 'software-engineering-unit-1-complete-notes-software-process-models-rgpv-cs-403',
  'status': 'published',
  'subject': 'Software Engineering',
  'title': 'Software Engineering Unit 1 Complete Notes | Software Process Models | RGPV CS-403',
  'unit': 'Unit 1',
  'updated_at': '2026-10-18T11:16:53.221734+00:00',
  'year': '2nd Year',
  'youtube_id': 'wG7sfHLWtjI',
  'youtube_url': 'https://www.youtube.com/watch?v=wG7sfHLWtjI'}]



def ensure_mongodb_initialized(db):
    """Ensure videos collection in MongoDB is indexed and populated."""
    if db is None:
        return
    try:
        db.videos.create_index("slug", unique=True)
        db.videos.create_index("youtube_id")
    except Exception:
        pass
    if db.videos.count_documents({}) == 0:
        print("[Database] Migrating initial video records into MongoDB...")
        for item in MIGRATED_VIDEOS:
            db.videos.insert_one(item.copy())
        print(f"[Database] Successfully migrated {len(MIGRATED_VIDEOS)} videos to MongoDB.")
    title_updates = [
        UpdateOne(
            {"youtube_id": youtube_id, "title": {"$ne": title}},
            {
                "$set": {
                    "title": title,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        for youtube_id, title in SIMPLIFIED_VIDEO_TITLES.items()
    ]
    result = db.videos.bulk_write(title_updates, ordered=False)
    if result.modified_count:
        print(f"[Database] Simplified titles for {result.modified_count} videos.")
