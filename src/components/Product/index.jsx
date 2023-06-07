import React from "react";
import "./Product.css";
import Progressbar from "../ProgressBar";

const Product = (props) => {
  const { title, cardImg, type, codes, count } = props;
  return (
    <div className="product">
      <ul className="product-container">
        <li className="product-container__item">
          <img src={cardImg} className="product-container__image" />
          <h4 className="product-container__title">
            {title}
            <span className="product-container__param">{type}</span>
          </h4>
          <span className="product-container__count">
            <Progressbar value={1} maxValue={count} type="goods" />
          </span>
          <button className="product-container__barcode">{codes[0]}</button>
        </li>
      </ul>
      {codes.length > 1 && (
        <ul className="product-container__barcode-list">
          <li className="product-container__barcode-list-item">
            <span className="product-container__count product-container__count_separate">
              <Progressbar value={0} maxValue={1} type="goods" />
            </span>
            <button className="product-container__barcode">{codes[1]}</button>
          </li>
          <li className="product-container__barcode-list-item">
            <span className="product-container__count product-container__count_separate">
              <Progressbar value={0} maxValue={1} type="goods" />
            </span>
            <button className="product-container__barcode">{codes[2]}</button>
          </li>
          <li className="product-container__barcode-list-item">
            <span className="product-container__count product-container__count_separate">
              <Progressbar value={0} maxValue={1} type="goods" />
            </span>
            <button className="product-container__barcode">{codes[3]}</button>
          </li>
        </ul>
      )}
    </div>
  );
};

export default Product;
