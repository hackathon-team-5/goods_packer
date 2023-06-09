import React from "react";
import Product from "../Product";
import "./Card.css";

const Card = (props) => {
  const { data } = props;
  let amount = 0;
  data.skus.map((obj) => (amount = amount + obj.amount));

  return (
    <div className="card-container">
      <h4 className="card-container__title">Упаковка {data.box_num}</h4>
      <ul className="card-container__list">
        <li className="card-container__list-item">
          <p className="card-container__list-item-paragraph">
            {amount} товаров
          </p>
        </li>
        <li className="card-container__list-item card-container__list-item_type">
          <p className="card-container__list-item-paragraph">
            Коробка {data.skus[0].recommended_cartontype.cartontype}
          </p>
        </li>
      </ul>
      {data.skus.map((card, index) => {
        return (
          <Product
            key={index}
            id={card.id}
            title={card.sku.sku}
            cardImg={card.sku.image}
            type={card.sku.cargotypes}
            count={card.amount}
          />
        );
      })}
    </div>
  );
};

export default Card;
