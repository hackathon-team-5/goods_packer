import "./Сompletion.css";
import ImageQualityIndexPath from "../../images/Quality_Index.svg";
import { Link } from "react-router-dom";
function Сompletion() {
  return (
    <div className="completion">
      <div className="completion__container">
        <img
          src={ImageQualityIndexPath}
          className="completion__img"
          alt="картинка успешной работы"
        />
        <h2 className="completion__header">Отличная работа!</h2>
        <p className="completion__text">
          Упакуйте товары и поставьте коробку на конвейер
        </p>
      </div>
      <button className="big-button completion__button">
        <Link className="completion__button-link" to="/">
          Готово
        </Link>
      </button>
    </div>
  );
}

export default Сompletion;
