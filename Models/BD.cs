namespace tp04.Models;
using Microsoft.Data.SqlClient;
using Dapper;
using tp04.Models;

public class bd
{       

   private string _connectionString =
@"Server=.\SQLEXPRESS;
Database=Album Virtual;
Integrated Security=True;
TrustServerCertificate=True;";

    public List<Figurita> ObtenerFiguritas()
    {
        List<Figurita> Figurita = new List <Figurita>();
        using(SqlConnection connection = new SqlConnection(_connectionString)){
string query = @"select 
                 F.id,
                 F.cantidadFiguritas, 
                 F.pegada,
                 J.id as idJugador,
                 J.nombre, 
                 J.posicion, 
                 S.pais, 
                 S.grupo 
                 from Figurita as F 
                 LEFT JOIN Jugador as J on F.idJugador = J.id 
                 LEFT JOIN Seleccion as S on J.idSeleccion = S.id";
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
public List<Figurita> ObtenerFiguritas(List<int> ids)
{
    List<Figurita> figuritas = new List<Figurita>();

    using(SqlConnection connection = new SqlConnection(_connectionString))
    {
        string query = @"select 
                         F.id,
                         F.cantidadFiguritas, 
                         F.pegada, 
                         J.id as idJugador,
                         J.nombre, 
                         J.posicion, 
                         S.pais, 
                         S.grupo 
                         from Figurita as F 
                         LEFT JOIN Jugador as J on F.idJugador = J.id 
                         LEFT JOIN Seleccion as S on J.idSeleccion = S.id
                         WHERE F.id IN @ids";

        figuritas = connection.Query<Figurita>(query, new { ids }).ToList();
    }

    return figuritas;
}

  public void PegarFigu(List<Figurita> Figuritas)
{
    using(SqlConnection connection = new SqlConnection(_connectionString))
    {
        connection.Open();

        foreach(Figurita figu in Figuritas)
        {
            string sql = @"SELECT pegada 
                           FROM Figurita 
                           WHERE id = @Id";

            bool pegada = connection.QueryFirst<bool>(sql, new { Id = figu.Id });


            if(pegada == false)
            {
                string pegar = @"UPDATE Figurita
                                 SET pegada = 1,
                                     cantidadFiguritas = cantidadFiguritas + 1
                                 WHERE id = @Id";

                connection.Execute(pegar, new { Id = figu.Id });
            }
            else
            {
                string sumar = @"UPDATE Figurita
                                 SET cantidadFiguritas = cantidadFiguritas + 1
                                 WHERE id = @Id";

                connection.Execute(sumar, new { Id = figu.Id });
            }
        }
    }
}

}