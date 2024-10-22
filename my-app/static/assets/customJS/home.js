const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);

function eliminarEmpleado(id_empleado, foto_empleado) {
  if (confirm("¿Estas seguro que deseas Eliminar el empleado?")) {
    let url = `/borrar-empleado/${id_empleado}/${foto_empleado}`;
    if (url) {
      window.location.href = url;
    }
  }
}




//libro
function eliminarLibro(id_libro) {
  if (confirm("¿Estas seguro que deseas Eliminar el libro?")) {
    let url = `/borrar-libro/${id_libro}`;
    if (url) {
      window.location.href = url;
    }
  }
}

function eliminarProducto(id_producto, foto_producto) {
  if (confirm("¿Estas seguro que deseas Eliminar el producto?")) {
    let url = `/borrar-producto/${id_producto}/${foto_producto}`;
    if (url) {
      window.location.href = url;
    }
  }
}
//mesa
function eliminarMesa(id_mesa) {
  if (confirm("¿Estas seguro que deseas Eliminar la mesa?")) {
    let url = `/borrar-mesa/${id_mesa}`;
    if (url) {
      window.location.href = url;
    }
  }
}

//reservaciones
function eliminarReserva(id_reserva) {
  if (confirm("¿Estas seguro que deseas Eliminar la reservacion?")) {
    let url = `/borrar-reserva/${id_reserva}`;
    console.log(`Redirigiendo a URL: ${url}`);
    if (url) {
      window.location.href = url;
    }
  }
}


//factura
function eliminarFactura(id) {
  if (confirm("¿Estas seguro que deseas Eliminar la factura?")) {
    let url = `/borrar-factura/${id}`;
    if (url) {
      window.location.href = url;
    }
  }
}