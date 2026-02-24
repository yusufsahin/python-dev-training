"""
Boston House veri seti ile lineer regresyon: train/test, StandardScaler, metrikler ve görselleştirme.
Denklem formülü (y = β₀ + Σ βᵢxᵢ) konsola ve grafikte gösterilir.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def load_boston_data():
    """Boston veri setini yükler; X (özellikler) ve y (hedef) döner. Pandas olmadan çalışır."""
    data = fetch_openml(name="boston", version=1, as_frame=False, parser="liac-arff")
    X = np.asarray(data.data, dtype=np.float64)
    y = np.asarray(data.target, dtype=np.float64).ravel()
    feature_names = (
        list(data.feature_names)
        if hasattr(data, "feature_names") and data.feature_names is not None
        else [f"x{i}" for i in range(X.shape[1])]
    )
    return X, y, feature_names


def print_equation(model, feature_names):
    """Lineer regresyon denklem formülünü konsola yazar: y = β₀ + β₁x₁ + ..."""
    intercept = model.intercept_
    coefs = model.coef_
    parts = [f"{intercept:.4f}"]
    for i, name in enumerate(feature_names):
        c = coefs[i]
        sign = "+" if c >= 0 else ""
        parts.append(f" {sign} {c:.4f}*{name}")
    formula = "y = " + "".join(parts)
    print("\n--- Regresyon denklemi (olceklenmis X ile) ---")
    print(formula)
    print("(Genel form: y = b0 + b1*x1 + b2*x2 + ... + bn*xn)")


def plot_results(y_test, y_pred, model, feature_names):
    """Actual vs Predicted, Residuals vs Predicted ve residual histogram; denklem formülü grafikte."""
    residuals = y_test - y_pred

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # 1) Actual vs Predicted
    ax1 = axes[0]
    ax1.scatter(y_test, y_pred, alpha=0.6, edgecolors="k", linewidths=0.5)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax1.plot(lims, lims, "r--", lw=2, label="y = x (45°)")
    ax1.set_xlabel("Gerçek (Actual)")
    ax1.set_ylabel("Tahmin (Predicted)")
    ax1.set_title("Actual vs Predicted")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect("equal", adjustable="box")

    # Denklem formülü (özet): grafikte kısa form
    eq_short = r"$y = \beta_0 + \sum_{i=1}^{n} \beta_i x_i$" + f"\n$\\beta_0$ = {model.intercept_:.2f}, n = {len(feature_names)} ozellik"
    ax1.text(0.05, 0.95, eq_short, transform=ax1.transAxes, fontsize=8, verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

    # 2) Residuals vs Predicted
    ax2 = axes[1]
    ax2.scatter(y_pred, residuals, alpha=0.6, edgecolors="k", linewidths=0.5)
    ax2.axhline(y=0, color="r", linestyle="--", lw=2)
    ax2.set_xlabel("Tahmin (Predicted)")
    ax2.set_ylabel("Artık (Residual)")
    ax2.set_title("Residuals vs Predicted")
    ax2.grid(True, alpha=0.3)

    # 3) Residual distribution
    ax3 = axes[2]
    ax3.hist(residuals, bins=20, edgecolor="black", alpha=0.7)
    ax3.axvline(x=0, color="r", linestyle="--", lw=2)
    ax3.set_xlabel("Artık (Residual)")
    ax3.set_ylabel("Frekans")
    ax3.set_title("Residual dağılımı")
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("boston_house_plots.png", dpi=150, bbox_inches="tight")
    plt.show()


def main():
    # Veri
    X, y, feature_names = load_boston_data()

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Ölçekleme (sadece train'e fit)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model
    model = LinearRegression().fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    # Metrikler
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("--- Test seti metrikleri ---")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"R2:   {r2:.4f}")

    # Denklem formülünü konsola yazdır
    print_equation(model, feature_names)

    # Grafikler (denklem formülü grafikte de)
    plot_results(y_test, y_pred, model, feature_names)


if __name__ == "__main__":
    main()
