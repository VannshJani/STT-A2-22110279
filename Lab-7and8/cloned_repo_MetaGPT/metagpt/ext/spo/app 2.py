import sys
from pathlib import Path

import streamlit as st
import yaml
from loguru import logger as _logger

sys.path.append(str(Path(__file__).parents[3]))

from metagpt.const import METAGPT_ROOT  # noqa: E402
from metagpt.ext.spo.components.optimizer import PromptOptimizer  # noqa: E402
from metagpt.ext.spo.utils.llm_client import SPO_LLM  # noqa: E402


def load_yaml_template(template_path):
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"prompt": "", "requirements": "", "count": None, "faq": [{"question": "", "answer": ""}]}


def save_yaml_template(template_path, data):
    template_format = {
        "prompt": str(data.get("prompt", "")),
        "requirements": str(data.get("requirements", "")),
        "count": data.get("count"),
        "faq": [
            {"question": str(faq.get("question", "")).strip(), "answer": str(faq.get("answer", "")).strip()}
            for faq in data.get("faq", [])
        ],
    }

    template_path.parent.mkdir(parents=True, exist_ok=True)

    with open(template_path, "w", encoding="utf-8") as f:
        yaml.dump(template_format, f, allow_unicode=True, sort_keys=False, default_flow_style=False, indent=2)


def main():
    st.title("SPO | Self-Supervised Prompt Optimization 🤖")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Configuration")

        # Template Selection/Creation
        settings_path = Path("metagpt/ext/spo/settings")
        existing_templates = [f.stem for f in settings_path.glob("*.yaml")]

        template_mode = st.radio("Template Mode", ["Use Existing", "Create New"])

        if template_mode == "Use Existing":
            template_name = st.selectbox("Select Template", existing_templates)
        else:
            template_name = st.text_input("New Template Name")
            if template_name and not template_name.endswith(".yaml"):
                template_name = f"{template_name}"

        # LLM Settings
        st.subheader("LLM Settings")
        opt_model = st.selectbox(
            "Optimization Model", ["claude-3-5-sonnet-20240620", "gpt-4o", "gpt-4o-mini", "deepseek-chat"], index=0
        )
        opt_temp = st.slider("Optimization Temperature", 0.0, 1.0, 0.7)

        eval_model = st.selectbox(
            "Evaluation Model", ["gpt-4o-mini", "claude-3-5-sonnet-20240620", "gpt-4o", "deepseek-chat"], index=0
        )
        eval_temp = st.slider("Evaluation Temperature", 0.0, 1.0, 0.3)

        exec_model = st.selectbox(
            "Execution Model", ["gpt-4o-mini", "claude-3-5-sonnet-20240620", "gpt-4o", "deepseek-chat"], index=0
        )
        exec_temp = st.slider("Execution Temperature", 0.0, 1.0, 0.0)

        # Optimizer Settings
        st.subheader("Optimizer Settings")
        initial_round = st.number_input("Initial Round", 1, 100, 1)
        max_rounds = st.number_input("Maximum Rounds", 1, 100, 10)

    # Main content area
    st.header("Template Configuration")

    if template_name:
        template_path = settings_path / f"{template_name}.yaml"
        template_data = load_yaml_template(template_path)

        if "current_template" not in st.session_state or st.session_state.current_template != template_name:
            st.session_state.current_template = template_name
            st.session_state.faqs = template_data.get("faq", [])

        # Edit template sections
        prompt = st.text_area("Prompt", template_data.get("prompt", ""), height=100)
        requirements = st.text_area("Requirements", template_data.get("requirements", ""), height=100)

        # FAQ section
        st.subheader("FAQ Examples")

        # Add new FAQ button
        if st.button("Add New FAQ"):
            st.session_state.faqs.append({"question": "", "answer": ""})

        # Edit FAQs
        new_faqs = []
        for i in range(len(st.session_state.faqs)):
            st.markdown(f"**FAQ #{i + 1}**")
            col1, col2, col3 = st.columns([45, 45, 10])

            with col1:
                question = st.text_area(
                    f"Question {i + 1}", st.session_state.faqs[i].get("question", ""), key=f"q_{i}", height=100
                )
            with col2:
                answer = st.text_area(
                    f"Answer {i + 1}", st.session_state.faqs[i].get("answer", ""), key=f"a_{i}", height=100
                )
            with col3:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.faqs.pop(i)
                    st.rerun()

            new_faqs.append({"question": question, "answer": answer})

        # Save template button
        if st.button("Save Template"):
            new_template_data = {"prompt": prompt, "requirements": requirements, "count": None, "faq": new_faqs}

            save_yaml_template(template_path, new_template_data)

            st.session_state.faqs = new_faqs
            st.success(f"Template saved to {template_path}")

        st.subheader("Current Template Preview")
        preview_data = {"prompt": prompt, "requirements": requirements, "count": None, "faq": new_faqs}
        st.code(yaml.dump(preview_data, allow_unicode=True), language="yaml")

        st.subheader("Optimization Logs")
        log_container = st.empty()

        class StreamlitSink:
            def write(self, message):
                current_logs = st.session_state.get("logs", [])
                current_logs.append(message.strip())
                st.session_state.logs = current_logs

                log_container.code("\n".join(current_logs), language="plaintext")

        streamlit_sink = StreamlitSink()
        _logger.remove()

        def prompt_optimizer_filter(record):
            return "optimizer" in record["name"].lower()

        _logger.add(
            streamlit_sink.write,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            filter=prompt_optimizer_filter,
        )
        _logger.add(METAGPT_ROOT / "logs/{time:YYYYMMDD}.txt", level="DEBUG")

        # Start optimization button
        if st.button("Start Optimization"):
            try:
                # Initialize LLM
                SPO_LLM.initialize(
                    optimize_kwargs={"model": opt_model, "temperature": opt_temp},
                    evaluate_kwargs={"model": eval_model, "temperature": eval_temp},
                    execute_kwargs={"model": exec_model, "temperature": exec_temp},
                )

                # Create optimizer instance
                optimizer = PromptOptimizer(
                    optimized_path="workspace",
                    initial_round=initial_round,
                    max_rounds=max_rounds,
                    template=f"{template_name}.yaml",
                    name=template_name,
                    iteration=True,
                )

                # Run optimization with progress bar
                with st.spinner("Optimizing prompts..."):
                    optimizer.optimize()

                st.success("Optimization completed!")

                st.header("Optimization Results")

                prompt_path = f"{optimizer.root_path}/prompts"
                result_data = optimizer.data_utils.load_results(prompt_path)

                for result in result_data:
                    round_num = result["round"]
                    success = result["succeed"]
                    prompt = result["prompt"]

                    with st.expander(f"Round {round_num} {':white_check_mark:' if success else ':x:'}"):
                        st.markdown("**Prompt:**")
                        st.code(prompt, language="text")
                        st.markdown("<br>", unsafe_allow_html=True)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Status:** {'Success ✅ ' if success else 'Failed ❌ '}")
                        with col2:
                            st.markdown(f"**Tokens:** {result['tokens']}")

                        st.markdown("**Answers:**")
                        for idx, answer in enumerate(result["answers"]):
                            st.markdown(f"**Question {idx + 1}:**")
                            st.text(answer["question"])
                            st.markdown("**Answer:**")
                            st.text(answer["answer"])
                            st.markdown("---")

                # Summary
                success_count = sum(1 for r in result_data if r["succeed"])
                total_rounds = len(result_data)

                st.markdown("### Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Rounds", total_rounds)
                with col2:
                    st.metric("Successful Rounds", success_count)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                _logger.error(f"Error during optimization: {str(e)}")


if __name__ == "__main__":
    main()
