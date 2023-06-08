import React from "react";
import Product from "../Product";
import "./Card.css";

const Card = (props) => {
  const { data } = props;
  return (
    <div className="card-container">
      <h4 className="card-container__title">Упаковка {data.packageInfo.id}</h4>
      <ul className="card-container__list">
        <li className="card-container__list-item">
          <p className="card-container__list-item-paragraph">
            {data.packageInfo.count} товара
          </p>
        </li>
        <li className="card-container__list-item card-container__list-item_type">
          <p className="card-container__list-item-paragraph">
            Коробка {data.packageInfo.type}
          </p>
        </li>
      </ul>
      {data.products.map((card, index) => {
        return (
          <Product
            key={index}
            title={card.title}
            cardImg={card.image}
            type={card.type}
            codes={card.barcode}
            count={card.count}
          />
        );
      })}
    </div>
  );
};

export default Card;
