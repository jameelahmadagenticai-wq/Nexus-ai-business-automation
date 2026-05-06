import streamlit as st

from api_client import (
    get_memories,
    delete_memory,
    update_memory
)

st.title("Memory Management")

# =========================
# LOAD MEMORIES
# =========================

memories = get_memories()

# =========================
# NORMALIZE RESPONSE
# =========================

memory_error = None

if isinstance(memories, dict):

    memory_error = memories.get("error")

    memories = (
        memories.get("results")
        or memories.get("memories")
        or []
    )

# =========================
# ERROR HANDLING
# =========================

if memory_error:

    st.warning(
        memory_error
    )

if not isinstance(memories, list):

    st.error(
        "Unexpected memory response format"
    )

    st.stop()

# =========================
# EMPTY CHECK
# =========================

if not memories:

    st.info("No memories found")

    st.stop()

# =========================
# DISPLAY MEMORIES
# =========================

for memory in memories:

    if not isinstance(memory, dict):

        continue

    memory_id = memory.get("id", "")

    memory_text = memory.get(
        "memory",
        memory.get(
            "content",
            memory.get(
                "text",
                ""
            )
        )
    )

    if not memory_id:

        memory_id = memory.get(
            "memory_id",
            ""
        )

    if not memory_id:

        st.info(memory_text)
        st.divider()
        continue

    st.subheader(
        f"Memory ID: {memory_id}"
    )

    updated_content = st.text_area(
        "Content",
        value=memory_text,
        key=memory_id
    )

    col1, col2 = st.columns(2)

    # =========================
    # UPDATE
    # =========================

    with col1:

        if st.button(
            "Update",
            key=f"update_{memory_id}"
        ):

            result = update_memory(
                memory_id,
                updated_content
            )

            if isinstance(result, dict) and "error" in result:

                st.error(result["error"])

            else:

                st.success(
                    "Memory updated"
                )

    # =========================
    # DELETE
    # =========================

    with col2:

        if st.button(
            "Delete",
            key=f"delete_{memory_id}"
        ):

            result = delete_memory(
                memory_id
            )

            if isinstance(result, dict) and "error" in result:

                st.error(result["error"])

            else:

                st.warning(
                    "Memory deleted"
                )

                st.rerun()

    st.divider()
