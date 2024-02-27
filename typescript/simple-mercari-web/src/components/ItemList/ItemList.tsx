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
  const [items, setItems] = useState<Item[]>([])
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
        onLoadCompleted && onLoadCompleted();
      })
      .catch(error => {
        console.error('GET error:', error)
      })
  }

  useEffect(() => {
    if (reload) {
      fetchItems();
    }
  }, [reload]);

  return (
    <div className="WholeList">
      {items.map((item) => {
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
  )
};