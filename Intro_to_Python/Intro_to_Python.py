
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, ImageColorGenerator

filename = "Data/Navneliste.txt"


#make counts of each letter with them as key
letter_counts = Counter()
length_counts = Counter()

filtered_letter_counts = Counter()
filtered_length_counts = Counter()

if __name__ == "__main__":
    #read file
    with open(filename) as f:
        content = f.readlines()

    #split the string by "," into names
    names = content[0].split(",")



    #sort names alphabetically
    names_sorted_alphabetically = sorted(names, key=str.lower)
    print("sorted alphabetically")
    print(names_sorted_alphabetically)

    #sort them by length
    names_sorted_by_length = sorted(names, key=len)
    print("sorted by length: ")
    print(names_sorted_by_length)

    #count letters in each name
    for name in names_sorted_alphabetically:
        letter_counts += Counter(name.lower())
        length_counts += Counter([str(len(name))])
    print("10 most common letters:")
    for letter in  letter_counts.most_common(10):
        print("letter {} occurs {} times".format(letter[0], letter[1]))


    #plot histograms and letter-cloud

    # fig/axes
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))

    # 1) Letter frequency (top-left)
    items = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
    letters, counts1 = zip(*items) if items else ([], [])
    sns.barplot(ax=axes[0, 0], x=list(letters), y=list(counts1), palette="mako")
    axes[0, 0].set(title="Letter Frequency", xlabel="Letter", ylabel="Count")
    if axes[0, 0].containers:
        axes[0, 0].bar_label(axes[0, 0].containers[0])

    # 2) Length frequency (top-right)
    items = sorted(length_counts.items(), key=lambda x: x[1], reverse=True)
    lengths, counts2 = zip(*items) if items else ([], [])
    sns.barplot(ax=axes[0, 1], x=list(lengths), y=list(counts2), palette="mako")
    axes[0, 1].set(title="Name Length Frequency", xlabel="Length", ylabel="Count")
    if axes[0, 1].containers:
        axes[0, 1].bar_label(axes[0, 1].containers[0])

    # 3) Word cloud (bottom-left)
    wc = WordCloud(
        width=800, height=400, background_color="white", colormap="mako"
    ).generate_from_frequencies(letter_counts)
    axes[1, 0].imshow(wc, interpolation="bilinear")
    axes[1, 0].axis("off")
    axes[1, 0].set_title("Letter Word Cloud")

    # 4) Boxplot of name lengths (bottom-right)
    # Option A: from names list (preferred if available)
    if "names" in globals() and names:
        lengths_for_box = [
            len(n.strip()) for n in names if isinstance(n, str) and n.strip()
        ]
    # Option B: reconstruct from length_counts dict
    else:
        lengths_for_box = [l for l, c in length_counts.items() for _ in range(c)]

    sns.boxplot(ax=axes[1, 1], y=lengths_for_box, color="#66c2a5")
    axes[1, 1].set(title="Distribution of Name Lengths", ylabel="Length (chars)")

    plt.tight_layout()
    plt.show()

    # Count most common name (case-insensitive)
    lower_case_names = [name.lower() for name in names]
    most_common_name = Counter(lower_case_names).most_common(1)
    print(
        "most common name is {} with an occurance of {} ".format(
            most_common_name[0][0], most_common_name[0][1]
        )
    )