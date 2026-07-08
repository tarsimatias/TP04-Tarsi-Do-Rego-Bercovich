namespace tp04.Models;
using Microsoft.Data.SqlClient;
using Dapper;
using tp04.Models;

public class bd
{       

    private string _connectionString = @"Server=localhost;
    DataBase=Album Virtual;Integrated Security=True;TrustServerCertificate=True;";

    public List<Figurita> ObtenerFiguritas()
    {
        List<Figurita> Figurita = new List <Figurita>();
        using(SqlConnection connection = new SqlConnection(_connectionString)){
            string query = "select F.cantidadFiguritas, F.pegada, J.id, J.nombre, J.posicion, S.pais, S.grupo from Figurita as F LEFT JOIN Jugador as J on F.idJugador = J.id LEFT JOIN Seleccion as S on J.idSeleccion = S.id";
            Figurita = connection.Query<Figurita>(query).ToList();
        }
        return Figurita;

    }

   public List<Figurita> ObtenerSobre()
{
    List<Figurita> todasfigus = ObtenerFiguritas();
    List<Figurita> SobreFigus = new List<Figurita>();
    var random = new Random();
    for (int i = 0; i < 5; i++)
    {
        int indiceAleatorio = random.Next(0, todasfigus.Count);
        SobreFigus.Add(todasfigus[indiceAleatorio]);
    }
    return SobreFigus;
}

    public void PegarFigu(List<Figurita> Figuritas)
    {
        foreach(Figurita figu in Figuritas) 
        {
            using(SqlConnection connection = new SqlConnection(_connectionString))
            {
            string query = "select pegada from Figurita where id = " + figu.id;
            bool pegada = connection.QuerySingleOrDefault<bool>(query);

            //hacer un update para q cantidad = cantidad + 1
            if(!pegada)
            {
                //hacer un update para q pegada = 1 (osea true)
            }

            //yo esto lo pense con que despues de que abras un sobre te aparezca el boton que te deja hacer esto.
            //esta funcion recibe la lista de "obtenersobre"
            //

            }

        }
    }



}