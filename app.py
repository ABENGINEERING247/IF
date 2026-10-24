from datetime import datetime
import sqlite3
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TaskFlow — Modern Task Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Black & Gold CSS Theme
st.markdown(
    """
<style>
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}
[data-testid="stSidebar"] {
    background-color: #080808;
    border-right: 1px solid rgba(255, 215, 0, 0.2);
}
.if-gradient {
    background: linear-gradient(90deg, #FFE066, #FFB700, #EAB308);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
div.stButton>button, div.stDownloadButton>button {
    border: 1px solid #FFD700 !important;
    background: linear-gradient(100deg, #EAB308, #CA8A04) !important;
    color: #000000 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}
div.stButton>button:hover {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.6) !important;
}
[data-testid="stMetric"] {
    background: rgba(15, 15, 15, 0.9);
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: 10px;
    padding: 12px;
}
[data-testid="stMetricValue"] {
    color: #FFD700 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# Database Initialization
DB_NAME = "tasks.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            completed INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


def add_task(title, description, priority):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, priority, completed, created_at)"
        " VALUES (?, ?, ?, 0, ?)",
        (title, description, priority, datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    conn.commit()
    conn.close()


def get_tasks(search_query="", priority_filter="All", status_filter="All"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT id, title, description, priority, completed, created_at FROM tasks WHERE 1=1"
    params = []

    if search_query:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if priority_filter != "All":
        query += " AND priority = ?"
        params.append(priority_filter)

    if status_filter == "Active":
        query += " AND completed = 0"
    elif status_filter == "Completed":
        query += " AND completed = 1"

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def toggle_task(task_id, current_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (0 if current_status == 1 else 1, task_id),
    )
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# Sidebar Navigation & Stats
with st.sidebar:
    st.markdown(
        '<h2>⚡ <span class="if-gradient">TASKFLOW</span></h2>',
        unsafe_allow_html=True,
    )
    st.caption("Modern SQLite Task Manager")
    st.divider()

    all_rows = get_tasks()
    total_tasks = len(all_rows)
    completed_tasks = sum(1 for r in all_rows if r[4] == 1)
    active_tasks = total_tasks - completed_tasks

    st.metric("Total Tasks", total_tasks)
    st.metric("Active", active_tasks)
    st.metric("Completed", completed_tasks)
    st.divider()
    st.caption("Built with Streamlit & SQLite • Black Edition")

# Main Interface
st.markdown(
    "# ⚡ <span class='if-gradient'>Task Management Hub</span>",
    unsafe_allow_html=True,
)
st.markdown(
    "Organize, prioritize, and track your daily work efficiently with local"
    " SQLite persistence."
)

# Add Task Section
with st.expander("➕ Add New Task", expanded=True):
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            task_title = st.text_input("Task Title *")
        with col2:
            task_priority = st.selectbox(
                "Priority", ["High", "Medium", "Low"], index=1
            )

        task_desc = st.text_area(
            "Description (Optional)",
            placeholder="Add details, links, or notes...",
        )
        submitted = st.form_submit_button("Create Task", use_container_width=True)

        if submitted:
            if task_title.strip():
                add_task(task_title.strip(), task_desc.strip(), task_priority)
                st.success(f"Task '{task_title}' added successfully!")
                st.rerun()
            else:
                st.error("Please provide a task title.")

st.divider()

# Search & Filter Controls
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    search_term = st.text_input(
        "🔍 Search Tasks", placeholder="Keyword in title or description..."
    )
with f_col2:
    priority_sel = st.selectbox(
        "Filter by Priority", ["All", "High", "Medium", "Low"]
    )
with f_col3:
    status_sel = st.selectbox("Filter by Status", ["All", "Active", "Completed"])

st.subheader("Your Tasks")
tasks = get_tasks(
    search_query=search_term,
    priority_filter=priority_sel,
    status_filter=status_sel,
)

if not tasks:
    st.info(
        "No tasks found. Use the 'Add New Task' form above to create your"
        " first task."
    )
else:
    for task in tasks:
        t_id, title, desc, priority, completed, created = task

        # Priority badge color coding
        badge_color = (
            "🔴"
            if priority == "High"
            else ("🟡" if priority == "Medium" else "🟢")
        )
        status_icon = "✅" if completed == 1 else "⏳"

        with st.container():
            col_a, col_b, col_c = st.columns([0.7, 0.15, 0.15])
            with col_a:
                display_title = (
                    f"~~{title}~~" if completed == 1 else f"**{title}**"
                )
                st.markdown(
                    f"{status_icon} {badge_color} **{priority} Priority** —"
                    f" {display_title}"
                )
                if desc:
                    st.caption(desc)
                st.text(f"Created: {created}")

            with col_b:
                btn_label = "Mark Active" if completed == 1 else "Complete"
                if st.button(
                    btn_label, key=f"toggle_{t_id}", use_container_width=True
                ):
                    toggle_task(t_id, completed)
                    st.rerun()

            with col_c:
                if st.button(
                    "🗑️ Delete", key=f"delete_{t_id}", use_container_width=True
                ):
                    delete_task(t_id)
                    st.success("Task deleted.")
                    st.rerun()

            st.divider()
