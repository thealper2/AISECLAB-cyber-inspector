function deleteQuery(id) {
    fetch("/delete-query", {
        method: "POST",
        body: JSON.stringify({ id: id}),
    }).then((_res) => {
        window.location.href = "/";
    });
}