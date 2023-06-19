import "./ProgressBar.css";
import { motion } from "framer-motion";

function Progressbar({ value, maxValue, type }) {
  const progressbarContainerGoods = `progressbar__container ${
    maxValue === 1
      ? "progressbar__container_size_small"
      : maxValue > 1 && maxValue < 9
      ? "progressbar__container_size_medium"
      : "progressbar__container_size_large"
  }`;

  const progressbarContainerAssembly = `progressbar__container progressbar__container_size_extralarge`;

  const progressbarTextTheme = `progressbar__text ${
    value !== maxValue || value === 0
      ? "progressbar__text_theme_dark"
      : "progressbar__text_theme_light"
  }`;

  const progressbarTextSize = `${
    maxValue > 99
      ? "progressbar__text_size_small"
      : "progressbar__text_size_large"
  }`;

  const progressbarBarGoods = `progressbar__bar ${
    value === maxValue
      ? "progressbar__bar_bright_dark"
      : "progressbar__bar_bright_light"
  }`;

  const progressbarBarAssembly = `progressbar__bar progressbar__bar_radius progressbar__bar_bright_dark`;

  return (
    <div
      className={
        type === "goods"
          ? progressbarContainerGoods
          : progressbarContainerAssembly
      }
    >
      <motion.div
        className={
          type === "goods" ? progressbarBarGoods : progressbarBarAssembly
        }
        animate={{
          width: `${value * (100 / maxValue)}%`,
        }}
        transition={{
          duration: 0.3,
        }}
      />
      {type === "goods" ? (
        <p className={progressbarTextTheme + " " + progressbarTextSize}>
          {maxValue > 1 ? `${value} из ${maxValue} шт.` : "1 шт."}
        </p>
      ) : (
        ""
      )}
    </div>
  );
}

export default Progressbar;
