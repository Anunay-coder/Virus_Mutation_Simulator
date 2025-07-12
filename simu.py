# install Streamlit using pip: pip install streamlit

import random
import streamlit as st
import matplotlib.pyplot as plt

# Define DNA bases
BASES = ['A', 'T', 'C', 'G']

# Generate initial random genome
def generate_genome(length=50):
    return ''.join(random.choices(BASES, k=length))

# Simulate mutation in a genome
def mutate_genome(genome, mutation_rate=0.05):
    mutated = ''
    for base in genome:
        if random.random() < mutation_rate:
            choices = [b for b in BASES if b != base]
            mutated += random.choice(choices)
        else:
            mutated += base
    return mutated

# Track mutations across generations
def simulate_generations(initial_genome, generations=20, mutation_rate=0.05):
    current_genome = initial_genome
    genomes = [current_genome]
    mutations = [0]

    for _ in range(generations):
        new_genome = mutate_genome(current_genome, mutation_rate)
        diff = sum(1 for a, b in zip(current_genome, new_genome) if a != b)
        mutations.append(mutations[-1] + diff)
        genomes.append(new_genome)
        current_genome = new_genome

    return genomes, mutations

# Streamlit GUI
st.set_page_config(page_title="Virus Mutation Simulator", page_icon="🧬", layout="centered")
st.title("🧬 Virus Mutation Simulator")
st.markdown(
    "Simulate how a virus genome mutates over generations. "
    "Adjust the parameters in the sidebar and see how mutation rates affect the genome and accumulated mutations."
)

with st.sidebar:
    st.header("Simulation Settings")
    length = st.slider("Genome Length", 10, 200, 50, help="Number of DNA bases in the genome.")
    mutation_rate = st.slider("Mutation Rate", 0.0, 1.0, 0.05, 0.01, help="Chance of mutation per base per generation.")
    generations = st.slider("Number of Generations", 1, 100, 20, help="How many generations to simulate.")

if st.button("Run Simulation", help="Click to run the mutation simulation with the selected settings."):
    initial_genome = generate_genome(length)
    genomes, mutations = simulate_generations(initial_genome, generations, mutation_rate)

    st.subheader("Initial Genome")
    st.code(initial_genome, language="text")

    st.subheader("Final Genome")
    st.code(genomes[-1], language="text")

    # Plot mutation curve
    fig, ax = plt.subplots()
    ax.plot(mutations, marker='o', color='blue', label='Original')
    ax.set_title("Accumulated Mutations Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Total Mutations")
    ax.grid(True)

    # Analyze mutation curve and give precautions
    mutation_total = mutations[-1]
    high_threshold = length * 0.7
    moderate_threshold = length * 0.3

    st.subheader("Precautionary Measures Suggestion")
    if mutation_total > high_threshold or mutation_rate > 0.3:
        st.error(
            "🔴 **High mutation accumulation detected!**\n\n"
            "Precautions:\n"
            "🔬 1. Strengthen Genomic Surveillance.\n"
            "💉 2. Adapt Vaccination Strategies.\n"
            "💊 3. Monitor Drug Resistance.\n"
            "😷 4. Reinforce Public Health Measures.\n"
            "📊 5. Increase Research Funding."
        )
        new_mutation_rate = max(0.01, mutation_rate * 0.5)
        precaution_level = "High"
    elif mutation_total > moderate_threshold or mutation_rate > 0.15:
        st.warning(
            "🟠 **Moderate mutation accumulation detected.**\n\n"
            "Precautions:\n"
            "💉 1. Maintain Vaccine Coverage and Monitoring.\n"
            "🧪 2. Monitor for Early Signs of Change.\n"
            "😷 3. Apply Targeted Public Health Measures.\n"
            "📈 4. Continue Research and Surveillance."
        )
        new_mutation_rate = max(0.01, mutation_rate * 0.7)
        precaution_level = "Moderate"
    else:
        st.success(
            "🟢 **Low mutation accumulation. Mutation stability achieved.**\n\n"
            "Precautions:\n"
            "✅ 1. Maintain Basic Surveillance\n"
            "💉 2. Ensure High Immunization Coverage.\n"
            "🌍 3. Strengthen Global Health Infrastructure.\n"
            "😷 4. Maintain Public Awareness and Hygiene Practices.\n"
        )
        new_mutation_rate = mutation_rate
        precaution_level = "Low"

    # Simulate after precautions if any change
    if new_mutation_rate != mutation_rate:
        # Simulate with new mutation rate for half the generations
        plateau_gens = generations // 2
        repair_gens = generations - plateau_gens

        genomes2, mutations2 = simulate_generations(initial_genome, plateau_gens, new_mutation_rate)
        # Plateau: keep the mutation count constant for a few generations
        plateau_mutation = mutations2[-1]
        plateau_genomes = [genomes2[-1]] * (repair_gens // 2)
        plateau_mutations = [plateau_mutation] * (repair_gens // 2)

        # Gradual decrease: simulate "repair" by reducing mutations
        decrease_mutations = []
        decrease_genomes = []
        current_mutation = plateau_mutation
        for i in range(repair_gens - len(plateau_mutations)):
            # Decrease mutations by a small amount each generation, not below zero
            current_mutation = max(0, current_mutation - max(1, plateau_mutation // repair_gens))
            decrease_mutations.append(current_mutation)
            decrease_genomes.append(genomes2[-1])  # For simplicity, genome stays the same

        # Combine all
        all_mutations2 = mutations2 + plateau_mutations + decrease_mutations
        all_genomes2 = genomes2 + plateau_genomes + decrease_genomes

        ax.plot(all_mutations2, marker='o', color='green', label='After Precaution')
        ax.legend()
        st.pyplot(fig)
        st.info(
            f"**After applying {precaution_level} precautions** (mutation rate set to {new_mutation_rate:.3f}):\n"
            f"- Final accumulated mutations: {all_mutations2[-1]}"
        )
        st.subheader("Final Genome After Precaution")
        st.code(all_genomes2[-1], language="text")
    else:
        ax.legend()
        st.pyplot(fig)

    with st.expander("🔎 All Genomes by Generation (Original)"):
        for i, g in enumerate(genomes):
            st.text(f"Gen {i:02}: {g}")

    if new_mutation_rate != mutation_rate:
        with st.expander("🔎 All Genomes by Generation (After Precaution)"):
            for i, g in enumerate(all_genomes2):
                st.text(f"Gen {i:02}: {g}")

    st.caption("Tip: Try increasing the mutation rate or generations to see how the precautions change!")
