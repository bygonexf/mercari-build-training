import React, { useEffect, useState } from 'react';

interface Item {
  id: number;
  name: string;
  category: string;
  image_name: string;
};

const server = process.env.REACT_APP_API_URL || 'http://127.0.0.1:9000';
const placeholderImage = process.env.PUBLIC_URL + '/logo192.png';

interface Prop {
  reload?: boolean;
  onLoadCompleted?: () => void;
}

export const ItemList: React.FC<Prop> = (props) => {
  const { reload = true, onLoadCompleted } = props;
  const [items, setItems] = useState<Item[]>([]);
  const [citems, setCItems] = useState<Item[]>([]);
  const fetchItems = () => {
    fetch(server.concat('/items'),
      {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      })
      .then(response => response.json())
      .then(data => {
        console.log('GET success:', data);
        data = JSON.parse(data)
        setItems(data.items);
        setCItems(data.items);
        onLoadCompleted && onLoadCompleted();
      })
      .catch(error => {
        console.error('GET error:', error)
      })
  }

  const onSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const filterKey = event.target.value;
    setCItems(items.filter(item => 
      item.name.toLowerCase().includes(filterKey.toLowerCase()) || item.category.toLowerCase().includes(filterKey.toLowerCase())
    ));
  };

  useEffect(() => {
    if (reload) {
      fetchItems();
    }
  }, [reload]);

  return (
    <div>

    <div className="input__container">
      <div className="shadow__input"></div>
      <button className="input__button__shadow">
        <svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" height="20px" width="20px">
          <path d="M4 9a5 5 0 1110 0A5 5 0 014 9zm5-7a7 7 0 104.2 12.6.999.999 0 00.093.107l3 3a1 1 0 001.414-1.414l-3-3a.999.999 0 00-.107-.093A7 7 0 009 2z" fill-rule="evenodd" fill="#17202A"></path>
        </svg>
      </button>
      <input type="text" className="input__search" placeholder="Search..." onChange={onSearchChange}/>
    </div>

    <div className="WholeList">
      {citems.map((item) => {
        return (
          
          <div key={item.id} className='ItemList'>
          <div className="card">
          <div className="card__img">
            <img
              className="InsideImage"
              src={server.concat('/image/', item.image_name)}
              onError={({ currentTarget }) => {
                currentTarget.onerror = null;
                currentTarget.src=placeholderImage;
              }}
              alt={item.name}
            />
          </div>
          <div className="card__subtitle">{item.category}</div>
          <div className="card__wrapper">
            <div className="card__title">{item.name}</div>
            <div className="card__icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 256 256"
                style={{
                  userSelect: "none",
                  width: "100%",
                  height: "100%",
                  display: "inline-block",
                  fill: "rgb(224, 223, 220)",
                  flexShrink: 0,
                  cursor: "auto"
                }}
                color="rgb(224, 223, 220)"
              >
                <g color="rgb(224, 223, 220)">
                  <circle cx={128} cy={128} r={96} opacity="0.2" />
                  <circle
                    cx={128}
                    cy={128}
                    r={96}
                    fill="none"
                    stroke="rgb(224, 223, 220)"
                    strokeMiterlimit={10}
                    strokeWidth={16}
                  />
                  <polyline
                    points="134.1 161.9 168 128 134.1 94.1"
                    fill="none"
                    stroke="rgb(224, 223, 220)"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={16}
                  />
                  <line
                    x1={88}
                    y1={128}
                    x2={168}
                    y2={128}
                    fill="none"
                    stroke="rgb(224, 223, 220)"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={16}
                  />
                </g>
              </svg>
            </div>
          </div>
          </div>
          </div>

        )
      })}
    </div>
    </div>
  )
};