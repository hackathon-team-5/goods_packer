export function getInfo() {
    return fetch('https://backend-hackaton.onrender.com/product', {
    method: 'GET',
  }).then(res => {
    if (res.ok) {
        return res.json()
    }
  })
  .catch(err => console.log(err))
}

export function orderAccept(sku, cargotype, amount, completed) {
  return fetch('https://backend-hackaton.onrender.com/product', {
    method: 'POST',
    body: JSON.stringify({
      sku: sku,
      cargotype: cargotype,
      amount: amount,
      completed: completed
    })
  })
}