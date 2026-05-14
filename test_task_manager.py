import unittest
from pathlib import Path

from task_manager import (
    add_task,
    complete_task,
    delete_task,
    filter_by_priority,
    get_summary,
    load_tasks,
    save_tasks,
    search_tasks,
)


class StudyTaskManagerTest(unittest.TestCase):
    def test_add_task_creates_valid_task(self):
        tasks = []

        task = add_task(tasks, "Finish assignment", "COMP9001", "2026-05-24", "High")

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Finish assignment")
        self.assertEqual(task["course"], "COMP9001")
        self.assertEqual(task["deadline"], "2026-05-24")
        self.assertEqual(task["priority"], "High")
        self.assertEqual(task["status"], "Not completed")
        self.assertEqual(len(tasks), 1)

    def test_add_task_rejects_invalid_date(self):
        tasks = []

        with self.assertRaises(ValueError):
            add_task(tasks, "Invalid date task", "COMP9001", "24-05-2026", "High")

    def test_file_io_saves_and_loads_tasks(self):
        tasks = []
        add_task(tasks, "Read textbook", "COMP9001", "2026-05-19", "Medium")

        filename = Path("test_tasks_temp.txt")
        try:
            save_tasks(tasks, filename)
            loaded_tasks = load_tasks(filename)
        finally:
            if filename.exists():
                filename.unlink()

        self.assertEqual(loaded_tasks, tasks)

    def test_complete_task_changes_status(self):
        tasks = []
        add_task(tasks, "Write tests", "COMP9001", "2026-05-20", "High")

        result = complete_task(tasks, 1)

        self.assertTrue(result)
        self.assertEqual(tasks[0]["status"], "Completed")

    def test_delete_task_removes_task(self):
        tasks = []
        add_task(tasks, "Delete me", "COMP9001", "2026-05-21", "Low")

        result = delete_task(tasks, 1)

        self.assertTrue(result)
        self.assertEqual(tasks, [])

    def test_search_tasks_finds_title_and_course(self):
        tasks = []
        add_task(tasks, "Python practice", "COMP9001", "2026-05-21", "High")
        add_task(tasks, "Math revision", "MATH1001", "2026-05-22", "Low")

        title_results = search_tasks(tasks, "python")
        course_results = search_tasks(tasks, "math1001")

        self.assertEqual(len(title_results), 1)
        self.assertEqual(title_results[0]["title"], "Python practice")
        self.assertEqual(len(course_results), 1)
        self.assertEqual(course_results[0]["course"], "MATH1001")

    def test_filter_by_priority(self):
        tasks = []
        add_task(tasks, "Important task", "COMP9001", "2026-05-21", "High")
        add_task(tasks, "Small task", "COMP9001", "2026-05-22", "Low")

        results = filter_by_priority(tasks, "High")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Important task")

    def test_summary_counts_tasks(self):
        tasks = []
        add_task(tasks, "Task one", "COMP9001", "2026-05-24", "High")
        add_task(tasks, "Task two", "COMP9001", "2026-05-24", "Medium")
        complete_task(tasks, 1)

        summary = get_summary(tasks)

        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["completed"], 1)
        self.assertEqual(summary["not_completed"], 1)


if __name__ == "__main__":
    unittest.main()
