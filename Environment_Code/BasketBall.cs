using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using UnityEngine.SceneManagement;

public class UDPReceive : MonoBehaviour
{
    public Rigidbody ball;
    public Transform target;
    public Transform target1;
    public float h = 5.5f;
    public float gravity = -18;

    Thread receiveThread;
    UdpClient client;
    public int port;
    public string lastReceivedUDPPacket = "";
    public string allReceivedUDPPackets = "";

    private static void Main()
    {
        UDPReceive receiveObj = new UDPReceive();
        receiveObj.init();

        string text = "";
        do
        {
            text = Console.ReadLine();
        }
        while (!text.Equals("exit"));
    }

    public void Start()
    {
        init();
        ball.useGravity = false;
    }


    void OnGUI()
    {
        Rect rectObj = new Rect(40, 10, 200, 400);
        GUIStyle style = new GUIStyle();
        style.alignment = TextAnchor.UpperLeft;
        GUI.Box(rectObj, "\nLast Packet: \n" + lastReceivedUDPPacket
                    + "\n\nAll Messages: \n" + allReceivedUDPPackets
                , style);

        Data move = new Data();
        move.movement = lastReceivedUDPPacket;

        if (string.Compare(move.movement, "1") == 0)
        {
            if (ball.transform.position = new Vector3(0, 2.82968f, 0))
            {
                LaunchLeft();
            }
        }

        if (string.Compare(move.movement, "2") == 0)
        {
            if (ball.transform.position = new Vector3(0, 2.82968f, 0))
            {
                LaunchRight();
            }
        }

    }

    void LaunchLeft()
    {
        Physics.gravity = Vector3.up * gravity;
        ball.useGravity = true;
        float displacementY = target1.position.y - ball.position.y;
        Vector3 displacementXZ = new Vector3(0, 0, target1.position.z - ball.transform.position.z);

        Vector3 velocityY = Vector3.up * Mathf.Sqrt(-2 * gravity * h);
        Vector3 velocityXZ = displacementXZ / (Mathf.Sqrt(-2 * h / gravity) + Mathf.Sqrt(2 * (displacementY - h) / gravity));

        ball.velocity = velocityXZ + velocityY;
        print(ball.velocity);

    }

    void LaunchRight()
    {
        Physics.gravity = Vector3.up * gravity;
        ball.useGravity = true;
        float displacementY = target.position.y - ball.position.y;
        Vector3 displacementXZ = new Vector3(target.position.x - ball.transform.position.x, 0, 0);

        Vector3 velocityY = Vector3.up * Mathf.Sqrt(-2 * gravity * h);
        Vector3 velocityXZ = displacementXZ / (Mathf.Sqrt(-2 * h / gravity) + Mathf.Sqrt(2 * (displacementY - h) / gravity));

        ball.velocity = velocityXZ + velocityY;
        print(ball.velocity);

    }

    private void init()
    {
        port = 5065;
        receiveThread = new Thread(
            new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);

                print(">> " + text);
                lastReceivedUDPPacket = text;
                allReceivedUDPPackets = allReceivedUDPPackets + text;
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }

    public string getLatestUDPPacket()
    {
        allReceivedUDPPackets = "";
        return lastReceivedUDPPacket;
    }
}
