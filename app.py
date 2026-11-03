
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import io

from pure_aloha import simulate_pure_aloha
from slotted_aloha import simulate_slotted_aloha


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ALOHA Protocol Simulator",
    page_icon="📡",
    layout="wide"
)

st.title("📡 ALOHA Protocol Simulator")

st.write(
    "A simulation-based comparison of Pure ALOHA "
    "and Slotted ALOHA random access protocols."
)

st.divider()


# ==========================================
# SIDEBAR SETTINGS
# ==========================================

st.sidebar.title("Simulation Settings")

traffic_load = st.sidebar.slider(
    "Offered Traffic Load (G)",
    min_value=0.1,
    max_value=2.0,
    value=0.5,
    step=0.1
)

total_frames = st.sidebar.number_input(
    "Number of frames / slots",
    min_value=1000,
    max_value=50000,
    value=10000,
    step=1000
)

run_button = st.sidebar.button(
    "Run Simulation",
    type="primary",
    use_container_width=True
)


# ==========================================
# SESSION STATE
# ==========================================

if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None

if "multi_load_results" not in st.session_state:
    st.session_state.multi_load_results = None


# ==========================================
# RUN MAIN SIMULATION
# ==========================================

if run_button:

    pure = simulate_pure_aloha(
        traffic_load,
        total_frames=int(total_frames)
    )

    slotted = simulate_slotted_aloha(
        traffic_load,
        total_slots=int(total_frames)
    )

    st.session_state.simulation_results = {
        "pure": pure,
        "slotted": slotted,
        "traffic_load": traffic_load,
        "total_frames": int(total_frames)
    }

    # Clear previous multiple-load results
    st.session_state.multi_load_results = None


# ==========================================
# DISPLAY RESULTS
# ==========================================

results = st.session_state.simulation_results

if results is None:

    st.info(
        "Adjust the simulation settings and click "
        "'Run Simulation' to view the results."
    )

else:

    pure = results["pure"]
    slotted = results["slotted"]
    selected_load = results["traffic_load"]
    selected_frames = results["total_frames"]

    st.success("Simulation completed successfully!")

    # ======================================
    # PERFORMANCE CALCULATIONS
    # ======================================

    pure_success_rate = (
        pure["successes"] / pure["attempts"] * 100
        if pure["attempts"] else 0
    )

    pure_collision_rate = (
        pure["collisions"] / pure["attempts"] * 100
        if pure["attempts"] else 0
    )

    slotted_success_rate = (
        slotted["successes"] / selected_frames * 100
    )

    slotted_collision_rate = (
        slotted["collisions"] / selected_frames * 100
    )

    slotted_idle_rate = (
        slotted["idle_slots"] / selected_frames * 100
    )


    # ======================================
    # 1. SIMULATION RESULTS
    # ======================================

    st.header("1. Simulation Results")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Pure ALOHA")

        st.metric(
            "Throughput",
            f"{pure['throughput']:.4f}"
        )

        st.metric(
            "Successful Frames",
            pure["successes"]
        )

        st.metric(
            "Success Rate",
            f"{pure_success_rate:.2f}%"
        )

        st.metric(
            "Collision Rate",
            f"{pure_collision_rate:.2f}%"
        )

    with col2:

        st.subheader("Slotted ALOHA")

        st.metric(
            "Throughput",
            f"{slotted['throughput']:.4f}"
        )

        st.metric(
            "Successful Frames",
            slotted["successes"]
        )

        st.metric(
            "Success Rate",
            f"{slotted_success_rate:.2f}%"
        )

        st.metric(
            "Collision Slot Rate",
            f"{slotted_collision_rate:.2f}%"
        )

        st.metric(
            "Idle Slots",
            slotted["idle_slots"]
        )

        st.metric(
            "Idle Slot Rate",
            f"{slotted_idle_rate:.2f}%"
        )


    st.divider()


    # ======================================
    # 2. THROUGHPUT COMPARISON GRAPH
    # ======================================

    st.header("2. Throughput Comparison Graph")

    loads = np.linspace(0.1, 2.0, 100)

    pure_theory = loads * np.exp(-2 * loads)
    slotted_theory = loads * np.exp(-loads)

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(
        loads,
        pure_theory,
        linestyle="--",
        label="Pure ALOHA Theory"
    )

    ax.plot(
        loads,
        slotted_theory,
        linestyle="--",
        label="Slotted ALOHA Theory"
    )

    ax.scatter(
        [selected_load],
        [pure["throughput"]],
        label="Pure ALOHA Simulation",
        marker="o",
        s=90
    )

    ax.scatter(
        [selected_load],
        [slotted["throughput"]],
        label="Slotted ALOHA Simulation",
        marker="s",
        s=90
    )

    ax.set_xlabel("Offered Traffic Load (G)")
    ax.set_ylabel("Throughput (S)")
    ax.set_title("Pure ALOHA vs Slotted ALOHA")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)


    st.divider()


    # ======================================
    # 3. AUTOMATIC PERFORMANCE ANALYSIS
    # ======================================

    st.header("3. Performance Analysis")

    if pure["throughput"] > slotted["throughput"]:

        better_protocol = "Pure ALOHA"

    elif slotted["throughput"] > pure["throughput"]:

        better_protocol = "Slotted ALOHA"

    else:

        better_protocol = "Both protocols have equal throughput"

    st.write(
        f"At offered traffic load G = {selected_load:.1f}, "
        f"the higher simulated throughput is "
        f"**{better_protocol}**."
    )

    st.write(
        f"Pure ALOHA throughput: "
        f"{pure['throughput']:.4f}"
    )

    st.write(
        f"Slotted ALOHA throughput: "
        f"{slotted['throughput']:.4f}"
    )

    st.info(
        "The theoretical maximum throughput is approximately "
        "0.184 for Pure ALOHA and 0.368 for Slotted ALOHA."
    )


    st.divider()


    # ======================================
    # 4. PROTOCOL COMPARISON TABLE
    # ======================================

    st.header("4. Protocol Comparison Table")

    comparison_data = pd.DataFrame({

        "Performance Metric": [
            "Offered Traffic Load",
            "Total Attempts",
            "Successful Frames",
            "Collisions",
            "Throughput",
            "Success Rate",
            "Collision Rate",
            "Idle Slots",
            "Idle Slot Rate"
        ],

        "Pure ALOHA": [
            f"{selected_load:.2f}",
            pure["attempts"],
            pure["successes"],
            pure["collisions"],
            f"{pure['throughput']:.4f}",
            f"{pure_success_rate:.2f}%",
            f"{pure_collision_rate:.2f}%",
            "N/A",
            "N/A"
        ],

        "Slotted ALOHA": [
            f"{selected_load:.2f}",
            slotted["attempts"],
            slotted["successes"],
            slotted["collisions"],
            f"{slotted['throughput']:.4f}",
            f"{slotted_success_rate:.2f}%",
            f"{slotted_collision_rate:.2f}%",
            slotted["idle_slots"],
            f"{slotted_idle_rate:.2f}%"
        ]
    })

    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ======================================
    # 5. THROUGHPUT BAR CHART
    # ======================================

    st.header("5. Throughput Bar Chart")

    fig2, ax2 = plt.subplots(figsize=(9, 4))

    protocols = [
        "Pure ALOHA",
        "Slotted ALOHA"
    ]

    throughput_values = [
        pure["throughput"],
        slotted["throughput"]
    ]

    bars = ax2.bar(
        protocols,
        throughput_values
    )

    ax2.bar_label(
        bars,
        fmt="%.4f",
        padding=4
    )

    ax2.set_ylabel("Throughput")

    ax2.set_title(
        f"Throughput Comparison at G = {selected_load:.2f}"
    )

    ax2.grid(axis="y")

    st.pyplot(fig2)
    plt.close(fig2)


    st.divider()


    # ======================================
    # 6. DOWNLOAD MAIN CSV RESULTS
    # ======================================

    st.header("6. Download Simulation Results")

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Protocol",
        "Offered Load",
        "Attempts",
        "Successes",
        "Collisions",
        "Idle Slots",
        "Throughput",
        "Success Rate (%)",
        "Collision Rate (%)"
    ])

    writer.writerow([
        "Pure ALOHA",
        selected_load,
        pure["attempts"],
        pure["successes"],
        pure["collisions"],
        "N/A",
        pure["throughput"],
        pure_success_rate,
        pure_collision_rate
    ])

    writer.writerow([
        "Slotted ALOHA",
        selected_load,
        slotted["attempts"],
        slotted["successes"],
        slotted["collisions"],
        slotted["idle_slots"],
        slotted["throughput"],
        slotted_success_rate,
        slotted_collision_rate
    ])

    st.download_button(
        label="📥 Download Results CSV",
        data=output.getvalue(),
        file_name="aloha_simulation_results.csv",
        mime="text/csv"
    )


    st.divider()


    # ======================================
    # 7. MULTIPLE TRAFFIC LOAD ANALYSIS
    # ======================================

    st.header("7. Multiple Traffic Load Analysis")

    st.write(
        "Compare Pure ALOHA and Slotted ALOHA "
        "at different offered traffic loads."
    )

    st.write(
        "This analysis tests 20 traffic-load values "
        "from 0.1 to 2.0."
    )

    analysis_frames = 5000

    if st.button(
        "Run Multiple Load Analysis",
        type="primary"
    ):

        test_loads = np.round(
            np.arange(0.1, 2.01, 0.1), 2
        )

        pure_results = []
        slotted_results = []

        progress = st.progress(0)

        for index, load in enumerate(test_loads):

            pure_result = simulate_pure_aloha(
                float(load),
                total_frames=analysis_frames,
                seed=100 + index
            )

            slotted_result = simulate_slotted_aloha(
                float(load),
                total_slots=analysis_frames,
                seed=200 + index
            )

            pure_results.append(
                pure_result["throughput"]
            )

            slotted_results.append(
                slotted_result["throughput"]
            )

            progress.progress(
                (index + 1) / len(test_loads)
            )

        progress.empty()

        st.session_state.multi_load_results = {
            "loads": test_loads.tolist(),
            "pure": pure_results,
            "slotted": slotted_results
        }

    # Display saved multiple-load analysis

    multi_results = st.session_state.multi_load_results

    if multi_results is not None:

        test_loads = np.array(multi_results["loads"])

        pure_results = multi_results["pure"]

        slotted_results = multi_results["slotted"]

        st.success(
            "Multiple traffic load analysis completed!"
        )

        # Multiple-load graph

        fig3, ax3 = plt.subplots(figsize=(11, 5))

        ax3.plot(
            test_loads,
            pure_results,
            marker="o",
            label="Pure ALOHA Simulation"
        )

        ax3.plot(
            test_loads,
            slotted_results,
            marker="s",
            label="Slotted ALOHA Simulation"
        )

        ax3.plot(
            test_loads,
            test_loads * np.exp(-2 * test_loads),
            linestyle="--",
            label="Pure ALOHA Theory"
        )

        ax3.plot(
            test_loads,
            test_loads * np.exp(-test_loads),
            linestyle="--",
            label="Slotted ALOHA Theory"
        )

        ax3.set_xlabel("Offered Traffic Load (G)")
        ax3.set_ylabel("Throughput (S)")

        ax3.set_title(
            "Throughput at Different Traffic Loads"
        )

        ax3.legend()
        ax3.grid(True)

        st.pyplot(fig3)
        plt.close(fig3)

        # Multiple-load table

        st.subheader("Traffic Load Results Table")

        load_data = pd.DataFrame({

            "Traffic Load (G)": test_loads,

            "Pure ALOHA Throughput": pure_results,

            "Slotted ALOHA Throughput": slotted_results

        })

        st.dataframe(
            load_data,
            use_container_width=True,
            hide_index=True
        )

        # Download multiple-load CSV

        load_csv = load_data.to_csv(index=False)

        st.download_button(
            label="📥 Download Multiple Load Results",
            data=load_csv,
            file_name="aloha_multiple_load_results.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "Click 'Run Multiple Load Analysis' "
            "to generate the graph and results table."
        )


    st.divider()


    # ======================================
    # 8. PROJECT INFORMATION
    # ======================================

    st.header("8. Project Information")

    st.markdown("""
    **Pure ALOHA**

    - Devices can transmit whenever they have data.
    - Frames can collide when their transmission times overlap.
    - Vulnerable period: two frame times.

    **Slotted ALOHA**

    - Devices transmit only at the beginning of a time slot.
    - Time synchronization reduces the vulnerable period.
    - Vulnerable period: one slot time.

    **Theoretical Throughput**

    - Pure ALOHA: S = G × e^(-2G)
    - Slotted ALOHA: S = G × e^(-G)
    """)

    st.caption(
        "Measurement note: Pure ALOHA collision counts are frames, "
        "while Slotted ALOHA collision counts are slots. "
        "The percentages therefore have different denominators."
    )
