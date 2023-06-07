import React from "react";
import "./Content.css";
import Progressbar from "../ProgressBar";
import Card from "../Card";

const Content = () => {
  return (
    <section className="content">
      <button className="big-button content__issue-button">
        Есть проблема
      </button>
      <div className="content__info-container">
        <h2 className="content__info-container-title">Сборка</h2>
        <div className="content__info-container-progress-bar">
          <Progressbar />
        </div>
        <h3 className="content__info-container-title_second">
          Сканируйте товары из ячейки
        </h3>
        <h4 className="content__info-container-title_number">B-09</h4>
        <ul className="content__info-container-list">
          <li className="content__info-container-list-item">
            <p className="content__info-container-list-item-paragraph">
              6 товаров
            </p>
          </li>
          <li className="content__info-container-list-item">
            <p className="content__info-container-list-item-paragraph">
              Почта России
            </p>
          </li>
        </ul>
        <Card />
      </div>
      <button className="big-button content__sucess-button">
        Закрыть упаковку
      </button>
    </section>
  );
};

export default Content;
