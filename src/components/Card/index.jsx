import React from "react";
import Product from "../Product";
import "./Card.css";
import speaker from "../../images/pic_product.png";

const codes = ["9234 5678 234 32"];

const Card = () => {
  return (
    <div className="card-container">
      <h4 className="card-container__title">Упаковка 1</h4>
      <ul className="card-container__list">
        <li className="card-container__list-item">
          <p className="card-container__list-item-paragraph">4 товара</p>
        </li>
        <li className="card-container__list-item card-container__list-item_type">
          <p className="card-container__list-item-paragraph">Коробка YMA</p>
        </li>
      </ul>
      <Product
        title="Умная колонка Яндекс Станция Лайт, ультрафиолет"
        cardImg={speaker}
        type="Пузырчатая плёнка"
        codes={codes}
        count={1}
      />
    </div>
  );
};

export default Card;
