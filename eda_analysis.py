"""
Sales & Performance EDA — FY 2026
Author: Ayush Bharati
MBA — Data Science & Business Analytics | LPU
Tools: Python, Pandas, NumPy, Matplotlib, Seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0f0f1a",
    "axes.facecolor": "#161628",
    "axes.edgecolor": "#2a2a50",
    "axes.labelcolor": "#c0c0d8",
    "xtick.color": "#7070a0",
    "ytick.color": "#7070a0",
    "text.color": "#e0e0f0",
    "grid.color": "#2a2a50",
    "grid.linewidth": 0.5,
    "font.family": "DejaVu Sans",
})
COLORS = ["#f2c811", "#4a90d9", "#00c875", "#e05050", "#00b4d8", "#9060d0", "#f0a040"]

# ── Load Data ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("  SALES & PERFORMANCE EDA — FY 2026")
print("  Analyst: Ayush Bharati | MBA Data Science & BA")
print("=" * 60)

df = pd.read_csv("../data/sales_2026.csv", parse_dates=["Date"])
print(f"\n✅ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns\n")

# ── 1. Data Quality Check ─────────────────────────────────────────────────────
print("─── 1. DATA QUALITY ─────────────────────────────────────")
print(f"  Null values: {df.isnull().sum().sum()}")
print(f"  Duplicates:  {df.duplicated().sum()}")
print(f"  Date range:  {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"  Data types:\n{df.dtypes.to_string()}\n")

# ── 2. Descriptive Statistics ─────────────────────────────────────────────────
print("─── 2. DESCRIPTIVE STATISTICS ───────────────────────────")
num_cols = ["UnitPrice", "Quantity", "Discount_Pct", "Revenue", "Margin_Pct", "Profit"]
print(df[num_cols].describe().round(2).to_string())
print()

# ── 3. Key Business KPIs ─────────────────────────────────────────────────────
print("─── 3. KEY BUSINESS KPIs ────────────────────────────────")
total_rev   = df["Revenue"].sum()
total_prof  = df["Profit"].sum()
total_ord   = len(df)
avg_order   = df["Revenue"].mean()
margin_pct  = total_prof / total_rev * 100
return_rate = df["Returned"].mean() * 100
unique_cust = df["CustomerID"].nunique()

print(f"  Total Revenue    : ₹{total_rev/1e7:.2f} Cr")
print(f"  Total Profit     : ₹{total_prof/1e7:.2f} Cr")
print(f"  Gross Margin     : {margin_pct:.1f}%")
print(f"  Total Orders     : {total_ord:,}")
print(f"  Avg Order Value  : ₹{avg_order:,.0f}")
print(f"  Return Rate      : {return_rate:.1f}%")
print(f"  Unique Customers : {unique_cust:,}")
print()

# ── 4. Revenue by Group ───────────────────────────────────────────────────────
print("─── 4. REVENUE BREAKDOWN ────────────────────────────────")
for grp in ["Category", "Region", "Channel", "Segment"]:
    g = (df.groupby(grp)["Revenue"]
         .sum().sort_values(ascending=False)
         .apply(lambda x: f"₹{x/1e7:.2f} Cr ({x/total_rev*100:.1f}%)"))
    print(f"\n  By {grp}:\n{g.to_string()}")
print()

# ── 5. Monthly Trend ─────────────────────────────────────────────────────────
print("─── 5. MONTHLY TREND ────────────────────────────────────")
monthly = (df.groupby("Month")
           .agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"), Orders=("OrderID","count"))
           .reindex(["January","February","March","April"]))
monthly["Margin_%"] = (monthly["Profit"] / monthly["Revenue"] * 100).round(1)
monthly["Revenue_Cr"] = (monthly["Revenue"] / 1e7).round(2)
print(monthly[["Revenue_Cr","Orders","Margin_%"]].to_string())
print()

# ── 6. Correlation Analysis ───────────────────────────────────────────────────
print("─── 6. CORRELATION MATRIX ───────────────────────────────")
corr = df[num_cols].corr().round(3)
print(corr.to_string())
print()

# ── 7. Statistical Tests ──────────────────────────────────────────────────────
print("─── 7. STATISTICAL TESTS ────────────────────────────────")
online  = df[df["Channel"] == "Online"]["Revenue"]
offline = df[df["Channel"] == "Offline"]["Revenue"]
t_stat, p_val = stats.ttest_ind(online, offline)
print(f"  T-test (Online vs Offline Revenue):")
print(f"    t-statistic = {t_stat:.4f},  p-value = {p_val:.4f}")
print(f"    Result: {'Significant difference' if p_val < 0.05 else 'No significant difference'} (α=0.05)\n")

cat_rev = [df[df["Category"]==c]["Revenue"].values for c in df["Category"].unique()]
f_stat, p_anova = stats.f_oneway(*cat_rev)
print(f"  One-Way ANOVA (Revenue across Categories):")
print(f"    F-statistic = {f_stat:.4f},  p-value = {p_anova:.6f}")
print(f"    Result: {'Significant difference' if p_anova < 0.05 else 'No significant difference'} across categories\n")

# ── 8. Visualizations ─────────────────────────────────────────────────────────
print("─── 8. GENERATING VISUALIZATIONS ───────────────────────")

fig = plt.figure(figsize=(20, 16))
fig.suptitle("Sales & Performance Analysis — FY 2026\nAnalyst: Ayush Bharati | MBA Data Science & Business Analytics",
             fontsize=16, fontweight="bold", color="#f2c811", y=0.98)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# Plot 1: Monthly Revenue vs Profit
ax1 = fig.add_subplot(gs[0, :2])
months_list = ["January","February","March","April"]
rev_m = [monthly.loc[m,"Revenue_Cr"] for m in months_list]
prof_m = [(monthly.loc[m,"Profit"]/1e7) for m in months_list]
x = np.arange(len(months_list))
w = 0.35
ax1.bar(x - w/2, rev_m, w, label="Revenue (₹Cr)", color=COLORS[0], alpha=0.85, edgecolor=COLORS[0])
ax1.bar(x + w/2, prof_m, w, label="Profit (₹Cr)", color=COLORS[2], alpha=0.85, edgecolor=COLORS[2])
ax1.set_title("Monthly Revenue vs Profit (₹ Cr)", fontweight="bold", pad=10)
ax1.set_xticks(x); ax1.set_xticklabels(months_list)
ax1.legend(fontsize=9); ax1.grid(axis="y", alpha=0.4)
for i, (r, p) in enumerate(zip(rev_m, prof_m)):
    ax1.text(i-w/2, r+0.05, f"₹{r}Cr", ha="center", fontsize=8, color=COLORS[0])
    ax1.text(i+w/2, p+0.05, f"₹{p:.2f}Cr", ha="center", fontsize=8, color=COLORS[2])

# Plot 2: Category pie
ax2 = fig.add_subplot(gs[0, 2])
cat_rev_vals = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
wedges, texts, autotexts = ax2.pie(cat_rev_vals.values, labels=cat_rev_vals.index,
        autopct="%1.1f%%", colors=COLORS[:4], startangle=90,
        wedgeprops=dict(edgecolor="#0f0f1a", linewidth=2))
for at in autotexts: at.set_fontsize(9); at.set_color("#0f0f1a")
ax2.set_title("Revenue by Category", fontweight="bold", pad=10)

# Plot 3: Region horizontal bar
ax3 = fig.add_subplot(gs[1, 0])
reg_rev = df.groupby("Region")["Revenue"].sum().sort_values() / 1e7
bars = ax3.barh(reg_rev.index, reg_rev.values, color=COLORS[:4][::-1], alpha=0.85, edgecolor="none")
ax3.set_title("Revenue by Region (₹ Cr)", fontweight="bold", pad=10)
ax3.set_xlabel("Revenue (₹ Cr)")
for bar, val in zip(bars, reg_rev.values):
    ax3.text(val + 0.05, bar.get_y() + bar.get_height()/2,
             f"₹{val:.2f}Cr", va="center", fontsize=9, color="#e0e0f0")
ax3.grid(axis="x", alpha=0.4)

# Plot 4: Segment revenue box plot
ax4 = fig.add_subplot(gs[1, 1])
segs = df["Segment"].unique()
seg_data = [df[df["Segment"]==s]["Revenue"].values for s in segs]
bp = ax4.boxplot(seg_data, labels=segs, patch_artist=True, notch=False,
                 medianprops=dict(color="#0f0f1a", linewidth=2))
for patch, color in zip(bp["boxes"], COLORS): patch.set_facecolor(color); patch.set_alpha(0.7)
ax4.set_title("Revenue Distribution by Segment", fontweight="bold", pad=10)
ax4.set_xlabel("Segment"); ax4.set_ylabel("Revenue (₹)")
ax4.tick_params(axis="x", labelsize=8)
ax4.grid(axis="y", alpha=0.4)

# Plot 5: Correlation heatmap
ax5 = fig.add_subplot(gs[1, 2])
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, ax=ax5, cmap="YlOrBr", annot=True, fmt=".2f",
            annot_kws={"size": 7}, linewidths=0.5, linecolor="#0f0f1a",
            cbar_kws={"shrink": 0.8})
ax5.set_title("Correlation Matrix", fontweight="bold", pad=10)
ax5.tick_params(labelsize=7)

# Plot 6: Return rate by category
ax6 = fig.add_subplot(gs[2, 0])
ret = df.groupby("Category")["Returned"].mean() * 100
bars6 = ax6.bar(ret.index, ret.values, color=COLORS[:4], alpha=0.85, edgecolor="none", width=0.5)
ax6.set_title("Return Rate by Category (%)", fontweight="bold", pad=10)
ax6.set_ylabel("Return Rate (%)"); ax6.set_ylim(0, 10)
for bar, val in zip(bars6, ret.values):
    ax6.text(bar.get_x()+bar.get_width()/2, val+0.1, f"{val:.1f}%",
             ha="center", fontsize=9, color="#e0e0f0")
ax6.grid(axis="y", alpha=0.4)

# Plot 7: Discount vs Revenue scatter
ax7 = fig.add_subplot(gs[2, 1])
sample = df.sample(500, random_state=42)
colors_map = {"Electronics": COLORS[0], "Furniture": COLORS[1],
              "Apparel": COLORS[2], "FMCG": COLORS[3]}
for cat, color in colors_map.items():
    mask_c = sample["Category"] == cat
    ax7.scatter(sample[mask_c]["Discount_Pct"], sample[mask_c]["Revenue"]/1000,
                c=color, alpha=0.5, s=20, label=cat)
m, b, r, p, _ = stats.linregress(df["Discount_Pct"], df["Revenue"]/1000)
x_line = np.linspace(0, 20, 100)
ax7.plot(x_line, m*x_line+b, color="white", linewidth=1.5, linestyle="--", alpha=0.7)
ax7.set_title(f"Discount vs Revenue (r={r:.3f})", fontweight="bold", pad=10)
ax7.set_xlabel("Discount %"); ax7.set_ylabel("Revenue (₹ K)")
ax7.legend(fontsize=7); ax7.grid(alpha=0.3)

# Plot 8: Channel margin comparison
ax8 = fig.add_subplot(gs[2, 2])
ch_margin = df.groupby("Channel")["Margin_Pct"].mean()
bars8 = ax8.bar(ch_margin.index, ch_margin.values, color=COLORS[:3], alpha=0.85, edgecolor="none", width=0.5)
ax8.set_title("Avg Margin % by Channel", fontweight="bold", pad=10)
ax8.set_ylabel("Gross Margin (%)"); ax8.set_ylim(30, 40)
for bar, val in zip(bars8, ch_margin.values):
    ax8.text(bar.get_x()+bar.get_width()/2, val+0.05, f"{val:.1f}%",
             ha="center", fontsize=9, color="#e0e0f0")
ax8.grid(axis="y", alpha=0.4)

plt.savefig("../dashboards/eda_visualizations.png", dpi=150, bbox_inches="tight",
            facecolor="#0f0f1a")
print("  ✅ Saved: dashboards/eda_visualizations.png")
plt.close()

print("\n" + "=" * 60)
print("  EDA COMPLETE")
print("=" * 60)
