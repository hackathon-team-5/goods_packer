import React, { useCallback, useContext, useEffect, useState } from "react";
import "./Product.css";
import Progressbar from "../ProgressBar";
import buttonIcon from "../../images/chevron.svg";
import { CardsContext } from "../../contexts/CardsContext";

const Product = (props) => {
  const { setCompletedCards } = useContext(CardsContext);
  const { id, title, cardImg, type, codes, count } = props;
  const [isShowList, setShowList] = useState(false);
  const [counter, setCount] = useState(0);

  useEffect(() => {
    if (count === counter) {
      setCompletedCards((prevCompletedCards) => [...prevCompletedCards, id]);
    }
  }, [counter]);

  const addNewItem = () => {
    if (counter < count) {
      setCount((prevCount) => prevCount + 1);
    } else {
      return;
    }
  };

  const generateRandomNumber = () => {
    let number = "";
    const template = "9234 5678 234 32";

    for (let i = 0; i < template.length; i++) {
      if (template[i] === " ") {
        number += " ";
      } else {
        number += Math.floor(Math.random() * 10);
      }
    }

    return number;
  };

  const handleShowList = useCallback(() => {
    setShowList((prevState) => !prevState);
  }, []);
  return (
    <div className="product">
      <ul className="product-container">
        <li className="product-container__item">
          <img src={cardImg} alt={title} className="product-container__image" />
          <h4 className="product-container__title">
            {title}
            {type.map((item, i) => {
              return (
                <span key={i} className="product-container__param">
                  {item.cargotype.description}
                </span>
              );
            })}
          </h4>
          <span className="product-container__count">
            <Progressbar value={counter} maxValue={count} type="goods" />
          </span>
          <button onClick={addNewItem} className="product-container__barcode">
            {generateRandomNumber()}
          </button>
          {/* {codes.length <= 1 ? (
            <button className="product-container__barcode">{codes}</button>
          ) : (
            <button
              type="button"
              onClick={handleShowList}
              className="product-container__barcode"
            >
              Свернуть
              <span>
                <img
                  className={
                    isShowList
                      ? "product-container__barcode-icon"
                      : "product-container__barcode-icon product-container__barcode-icon_active"
                  }
                  src={buttonIcon}
                  alt=""
                />
              </span>
            </button>
          )} */}
        </li>
      </ul>
      {/* {isShowList && codes.length > 1 && (
        <ul className="product-container__barcode-list">
          <li className="product-container__item product-container__barcode-list-item">
            <span className="product-container__count product-container__count_separate">
              <Progressbar value={1} maxValue={1} type="goods" />
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
      )} */}
    </div>
  );
};

export default Product;
